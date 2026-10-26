import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { apiRequest } from '../api/client'
import { HealthPage } from './HealthPage'

vi.mock('../api/client', () => ({
  apiRequest: vi.fn(),
}))

const mockedApiRequest = vi.mocked(apiRequest)

describe('HealthPage', () => {
  beforeEach(() => {
    mockedApiRequest.mockReset()
  })

  it('shows the server status when the request succeeds', async () => {
    mockedApiRequest.mockResolvedValue({ status: 'ok' })

    render(<HealthPage />)

    expect(
      await screen.findByText('서버가 정상적으로 연결되었습니다.'),
    ).toBeTruthy()
    expect(screen.getByText('응답 상태: ok')).toBeTruthy()
  })

  it('shows a useful message when the request fails', async () => {
    mockedApiRequest.mockRejectedValue(new Error('서버에 연결할 수 없습니다.'))

    render(<HealthPage />)

    expect(await screen.findByRole('alert')).toBeTruthy()
    expect(screen.getByText('서버에 연결할 수 없습니다.')).toBeTruthy()
  })
})
