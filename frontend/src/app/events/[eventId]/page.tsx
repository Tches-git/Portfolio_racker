import { redirect } from 'next/navigation'

export default async function EventDetailRedirect({ params }: { params: Promise<{ eventId: string }> }) {
  const { eventId } = await params
  redirect(`/events?view=events&selected_event_id=${encodeURIComponent(eventId)}`)
}
