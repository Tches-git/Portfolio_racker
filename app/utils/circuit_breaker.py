"""熔断器 — 防止对持续故障的外部服务重复调用"""
from __future__ import annotations

import time
import threading
from dataclasses import dataclass, field
from enum import Enum


class CircuitState(Enum):
    """熔断器状态"""
    CLOSED = "closed"        # 正常（允许调用）
    OPEN = "open"            # 熔断（拒绝请求）
    HALF_OPEN = "half_open"  # 试探恢复（允许一次试探调用）


class CircuitOpenError(Exception):
    """熔断器开启时的异常"""

    def __init__(self, name: str, retry_after: float):
        self.name = name
        self.retry_after = retry_after
        super().__init__(f"熔断器 {name} 已开启，{retry_after:.0f}秒后重试")


class CircuitBreaker:
    """轻量级熔断器

    - failure_threshold: 连续失败 N 次后开启熔断
    - recovery_timeout: 熔断后等待 N 秒进入 half_open
    - 线程安全
    """

    def __init__(self, name: str, failure_threshold: int = 3, recovery_timeout: float = 60.0):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self._lock = threading.Lock()
        self._state = CircuitState.CLOSED
        self._consecutive_failures = 0
        self._last_failure_time: float = 0.0

        # 统计
        self._total_calls = 0
        self._total_failures = 0
        self._total_circuit_opens = 0

    @property
    def state(self) -> CircuitState:
        """返回当前状态（考虑 recovery_timeout 自动转换）"""
        with self._lock:
            if self._state == CircuitState.OPEN:
                if time.time() - self._last_failure_time >= self.recovery_timeout:
                    self._state = CircuitState.HALF_OPEN
            return self._state

    @property
    def stats(self) -> dict[str, int]:
        """返回调用统计"""
        with self._lock:
            return {
                "total_calls": self._total_calls,
                "total_failures": self._total_failures,
                "circuit_opens": self._total_circuit_opens,
            }

    def call(self, func, *args, **kwargs):
        """通过熔断器执行函数，熔断时抛出 CircuitOpenError"""
        with self._lock:
            self._total_calls += 1

            # 检查 OPEN → HALF_OPEN 时间转换
            if self._state == CircuitState.OPEN:
                elapsed = time.time() - self._last_failure_time
                if elapsed >= self.recovery_timeout:
                    self._state = CircuitState.HALF_OPEN
                else:
                    retry_after = self.recovery_timeout - elapsed
                    raise CircuitOpenError(self.name, retry_after)

        # CLOSED 或 HALF_OPEN：执行实际调用（锁外执行，避免阻塞其他线程）
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            self._on_failure()
            raise
        else:
            self._on_success()
            return result

    def _on_success(self) -> None:
        """调用成功：重置连续失败计数，HALF_OPEN → CLOSED"""
        with self._lock:
            self._consecutive_failures = 0
            if self._state == CircuitState.HALF_OPEN:
                self._state = CircuitState.CLOSED

    def _on_failure(self) -> None:
        """调用失败：累加失败计数，达阈值则熔断"""
        with self._lock:
            self._consecutive_failures += 1
            self._total_failures += 1
            self._last_failure_time = time.time()

            if self._state == CircuitState.HALF_OPEN:
                # 试探失败 → 重新 OPEN
                self._state = CircuitState.OPEN
                self._total_circuit_opens += 1
            elif self._consecutive_failures >= self.failure_threshold:
                self._state = CircuitState.OPEN
                self._total_circuit_opens += 1

    def reset(self) -> None:
        """手动重置熔断器到 CLOSED 状态"""
        with self._lock:
            self._state = CircuitState.CLOSED
            self._consecutive_failures = 0
            self._last_failure_time = 0.0
