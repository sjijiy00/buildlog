import { useEffect, useState } from 'react'

import { apiRequest } from '../api/client'

type HealthResponse = {
  status: string
}

type HealthState =
  | { type: 'loading' }
  | { type: 'success'; status: string }
  | { type: 'error'; message: string }

export function HealthPage() {
  const [state, setState] = useState<HealthState>({ type: 'loading' })

  useEffect(() => {
    let active = true

    apiRequest<HealthResponse>('/api/health')
      .then((data) => {
        if (active) {
          setState({ type: 'success', status: data.status })
        }
      })
      .catch((error: unknown) => {
        if (active) {
          const message =
            error instanceof Error
              ? error.message
              : '서버 상태를 확인하지 못했습니다.'
          setState({ type: 'error', message })
        }
      })

    return () => {
      active = false
    }
  }, [])

  return (
    <section className="status-section" aria-labelledby="status-title">
      <p className="eyebrow">BUILDLOG 시작하기</p>
      <h1 id="status-title">서버 연결 확인</h1>
      <p className="page-description">
        화면과 서버가 서로 요청을 주고받을 준비가 되었는지 확인합니다.
      </p>

      <div className="status-card">
        {state.type === 'loading' && (
          <p className="status-message">서버 상태를 확인하고 있습니다.</p>
        )}

        {state.type === 'success' && (
          <div className="status-result status-result--success" role="status">
            <span className="status-dot" aria-hidden="true" />
            <div>
              <strong>서버가 정상적으로 연결되었습니다.</strong>
              <p>응답 상태: {state.status}</p>
            </div>
          </div>
        )}

        {state.type === 'error' && (
          <div className="status-result status-result--error" role="alert">
            <span className="status-dot" aria-hidden="true" />
            <div>
              <strong>서버에 연결하지 못했습니다.</strong>
              <p>{state.message}</p>
            </div>
          </div>
        )}
      </div>
    </section>
  )
}
