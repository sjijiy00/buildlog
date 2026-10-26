import { NavLink, Outlet } from 'react-router-dom'

export function Layout() {
  return (
    <div className="app-shell">
      <header className="site-header">
        <div className="header-inner">
          <NavLink className="brand" to="/">
            BuildLog
          </NavLink>
          <nav aria-label="주 메뉴">
            <NavLink className="nav-link" to="/">
              서버 상태
            </NavLink>
          </nav>
        </div>
      </header>

      <main className="page-content">
        <Outlet />
      </main>
    </div>
  )
}
