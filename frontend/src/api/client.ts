export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

function getErrorMessage(payload: unknown): string | null {
  if (typeof payload !== 'object' || payload === null) {
    return null
  }

  const body = payload as { detail?: unknown; message?: unknown }
  if (typeof body.detail === 'string') {
    return body.detail
  }
  if (typeof body.message === 'string') {
    return body.message
  }
  return null
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers)
  if (options.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }

  let response: Response
  try {
    response = await fetch(path, {
      ...options,
      credentials: 'include',
      headers,
    })
  } catch {
    throw new ApiError('서버에 연결할 수 없습니다.', 0)
  }

  if (!response.ok) {
    let payload: unknown
    try {
      payload = await response.json()
    } catch {
      payload = null
    }

    throw new ApiError(
      getErrorMessage(payload) ?? '요청을 처리하지 못했습니다.',
      response.status,
    )
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json() as Promise<T>
}
