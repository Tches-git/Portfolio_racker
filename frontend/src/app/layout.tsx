import './globals.css'
import type { ReactNode } from 'react'

import { AppShell } from '../components/app-shell'
import { GlobalRunCenter } from '../components/global-run-center'

export const metadata = {
  title: 'AI Research Assistant',
  description: 'Product-grade frontend shell for the research assistant',
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
