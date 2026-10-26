import { Route, Routes } from 'react-router-dom'

import { Layout } from './components/Layout'
import { HealthPage } from './pages/HealthPage'

export function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<HealthPage />} />
      </Route>
    </Routes>
  )
}
