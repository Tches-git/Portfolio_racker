'use client'

import type { ReactNode } from 'react'

import { SidebarNav } from './sidebar-nav'

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="appFrame">
      <aside className="sidebar">
        <div>
          <div className="brandMark">AI</div>
          <div className="brandTitle">Research OS</div>
          <div className="brandSub">研究、任务与交付的一体化工作台</div>
        </div>

        <SidebarNav />

        <div className="sidebarCard">
          <div className="sidebarCardTitle">当前阶段</div>
          <div className="sidebarCardText">兼容前端演进：保留 Python 引擎与 CLI / API 链路，通过独立工作台持续补任务中心、详情工作区与交付视图。</div>
        </div>
      </aside>

      <div className="contentArea">{children}</div>
    </div>
  )
}
