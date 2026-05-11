from __future__ import annotations

import time

import pytest

from app.utils.circuit_breaker import CircuitBreaker, CircuitOpenError, CircuitState


def test_circuit_opens_after_threshold_failures():
    breaker = CircuitBreaker("test", failure_threshold=2, recovery_timeout=0.1)

    def boom():
        raise RuntimeError("fail")

    with pytest.raises(RuntimeError):
        breaker.call(boom)
    assert breaker.state == CircuitState.CLOSED

    with pytest.raises(RuntimeError):
        breaker.call(boom)
    assert breaker.state == CircuitState.OPEN

    with pytest.raises(CircuitOpenError):
        breaker.call(lambda: "ok")


def test_circuit_recovers_after_timeout():
    breaker = CircuitBreaker("test", failure_threshold=1, recovery_timeout=0.05)

    with pytest.raises(RuntimeError):
        breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
    assert breaker.state == CircuitState.OPEN

    time.sleep(0.06)
    assert breaker.state == CircuitState.HALF_OPEN

    result = breaker.call(lambda: "ok")
    assert result == "ok"
    assert breaker.state == CircuitState.CLOSED


def test_half_open_failure_reopens_circuit():
    breaker = CircuitBreaker("test", failure_threshold=1, recovery_timeout=0.05)

    with pytest.raises(RuntimeError):
        breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))

    time.sleep(0.06)
    assert breaker.state == CircuitState.HALF_OPEN

    with pytest.raises(RuntimeError):
        breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail-again")))
    assert breaker.state == CircuitState.OPEN
