import { Link, Outlet, NavLink, useLocation, useNavigate } from "react-router-dom";
import { clearToken, api } from "../api/client";
import { useEffect, useState } from "react";

export default function DashboardLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const [userInfo, setUserInfo] = useState(null);

  const topbarTitle = {
    "/app": "Dashboard",
    "/app/generate": "Generate",
    "/app/history": "History",
    "/app/analytics": "Analytics",
    "/app/plans": "Plans & Credits",
  }[location.pathname] || "Dashboard";

  useEffect(() => {
    api.get("/auth/me")
      .then((data) => setUserInfo(data))
      .catch(() => setUserInfo(null));
  }, [location.pathname]); // refresh on page change so deductions show up

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

          <NavLink
            to="/app/plans"
            className={({ isActive }) =>
              isActive ? "navItem navItemActive" : "navItem"
            }
          >
            Plans &amp; Credits
          </NavLink>
        </nav>

        <div style={{ marginTop: "auto" }}>
          <div className="credits">
            <span style={{ textTransform: "capitalize" }}>
              {userInfo?.subscription_tier || "free"}
            </span>
            <span className="pill">
              {userInfo !== null ? `${userInfo.credits} credits` : "..."}
            </span>
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
          <span className="pill">
            {userInfo !== null ? `${userInfo.credits} credits` : "..."}
          </span>
        </div>

        <div className="contentPanel">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
