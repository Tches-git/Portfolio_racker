import type { ReactNode } from 'react'

import type { WorkbenchAction } from '../../lib/types'
import { WorkbenchActionButtons } from './workbench-action-buttons'

export function WorkspaceShell({
  eyebrow,
  title,
  description,
  actions = [],
  children,
}: {
  eyebrow: string
  title: string
  description?: string
  actions?: WorkbenchAction[]
  children: ReactNode
}) {
  return (
    <main className="wbPage">
      <header className="wbHeader">
        <div>
          <div className="wbEyebrow">{eyebrow}</div>
          <h1>{title}</h1>
          {description ? <p>{description}</p> : null}
        </div>
        {actions.length ? <WorkbenchActionButtons actions={actions} /> : null}
      </header>
      {children}
    </main>
  )
}
