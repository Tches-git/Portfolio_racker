import type { ReactNode } from 'react'

import type { WorkbenchAction } from '../../lib/types'
import { PageShell } from './primitives'

export function WorkspaceShell({
  eyebrow,
  title,
  description,
  actions = [],
  className = '',
  compact = false,
  children,
}: {
  eyebrow: string
  title: string
  description?: string
  actions?: WorkbenchAction[]
  className?: string
  compact?: boolean
  children: ReactNode
}) {
  return (
    <PageShell eyebrow={eyebrow} title={title} description={description} actions={actions} className={className} compact={compact}>
      {children}
    </PageShell>
  )
}
