import { WatchlistCreateForm } from '../watchlist-create-form'
import type { DashboardSetup } from '../../lib/types'

export function SetupWizard({ setup }: { setup: DashboardSetup }) {
  return (
    <section className="wbSetup">
      <div className="wbSetupIntro">
        <div className="wbEyebrow">新工作区 · 创建第一个组合</div>
        <h2>{setup.title}</h2>
        <p>{setup.description}</p>
        <div className="wbHintList">
          <span>1. 输入组合名称和股票代码</span>
          <span>2. 手动刷新组合事件</span>
          <span>3. 在驾驶舱处理预警和研报动作</span>
        </div>
      </div>
      <div className="wbPanel wbSetupForm">
        <WatchlistCreateForm />
      </div>
    </section>
  )
}
