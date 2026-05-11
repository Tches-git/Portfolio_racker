import './globals.css'
import type { ReactNode } from 'react'

import { AppShell } from '../components/app-shell'
import { GlobalRunCenter } from '../components/global-run-center'

export const metadata = {
  title: '金融消息追踪平台',
  description: '组合事件、预警处理与研报交付工作台',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>
        <AppShell>
          <GlobalRunCenter />
          {children}
        </AppShell>
      </body>
    </html>
  )
}
