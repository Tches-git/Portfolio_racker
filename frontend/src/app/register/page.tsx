import { RegisterForm } from '../../components/auth-forms'

type AuthPageProps = {
  searchParams?: Promise<{ next?: string }>
}

export default async function RegisterPage({ searchParams }: AuthPageProps) {
  const params = await searchParams
  return (
    <main className="authPage">
      <RegisterForm nextPath={safeNextPath(params?.next)} />
    </main>
  )
}

function safeNextPath(nextPath = '/') {
  return nextPath.startsWith('/') && !nextPath.startsWith('//') ? nextPath : '/'
}
