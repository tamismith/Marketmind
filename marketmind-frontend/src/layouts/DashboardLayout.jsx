import { Link, Outlet, NavLink, useLocation, useNavigate } from "react-router-dom";
import { clearToken } from "../api/client";
export default function DashboardLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const topbarTitle = {
    "/app": "Dashboard",
    "/app/generate": "Generate",
    "/app/history": "History",
    "/app/analytics": "Analytics",
  }[location.pathname] || "Dashboard";

  return (
    <div className="shell">
      <aside className="sidebar">
        <Link to="/" className="brand link" style={{ textDecoration: "none" }}>
          MarketMind
        </Link>

        <nav className="nav">
          <NavLink
            to="/app"
            end
            className={({ isActive }) =>
              isActive ? "navItem navItemActive" : "navItem"
            }
          >
            Dashboard
          </NavLink>

          <NavLink
            to="/app/generate"
            className={({ isActive }) =>
              isActive ? "navItem navItemActive" : "navItem"
            }
          >
            Generate
          </NavLink>

          <NavLink
            to="/app/history"
            className={({ isActive }) =>
              isActive ? "navItem navItemActive" : "navItem"
            }
          >
            History
          </NavLink>

          <NavLink
            to="/app/analytics"
            className={({ isActive }) =>
              isActive ? "navItem navItemActive" : "navItem"
            }
          >
            Analytics
          </NavLink>
        </nav>

        <div style={{ marginTop: "auto" }}>
          <div className="credits">
            <span>Credits</span>
            <span className="pill">38/50 left</span>
          </div>

          <button
            className="logout"
            onClick={() => {
              clearToken();
              navigate("/login");
            }}
          >
            Logout
          </button>
        </div>
      </aside>

      <main className="main">
        <div className="topbar">
          <h2 style={{ margin: 0 }}>{topbarTitle}</h2>
          <span className="pill">38 credits</span>
        </div>

        <div className="contentPanel">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
