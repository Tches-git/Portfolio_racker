export function LoadingSkeleton({ sections = 3 }: { sections?: number }) {
  return (
    <div className="grid">
      {Array.from({ length: sections }).map((_, index) => (
        <section key={index} className={`panel ${index === 0 ? 'span-7' : 'span-5'} skeletonPanel`}>
          <div className="skeletonLine skeletonLineShort" />
          <div className="skeletonCard">
            <div className="skeletonLine skeletonLineMedium" />
            <div className="skeletonLine" />
            <div className="skeletonLine" />
          </div>
        </section>
      ))}
      <section className="panel span-12 skeletonPanel">
        <div className="skeletonLine skeletonLineShort" />
        <div className="skeletonTable">
          <div className="skeletonLine" />
          <div className="skeletonLine" />
          <div className="skeletonLine" />
        </div>
      </section>
    </div>
  )
}
