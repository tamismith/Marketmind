import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import DashboardLayout from "./layouts/DashboardLayout.jsx";
import DashboardHome from "./pages/DashboardHome.jsx";
import Generate from "./pages/Generate.jsx";
import History from "./pages/History.jsx";
import Analytics from "./pages/Analytics.jsx";
import Plans from "./pages/Plans.jsx";
import Brand from "./pages/Brand.jsx";
import Campaigns from "./pages/Campaigns.jsx";
import NotFound from "./pages/NotFound.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";


export default function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/" element={<Home />} />
      <Route
        path="/login"
        element={<Login />}
      />
      <Route
        path="/register"
        element={<Register />}
      />

      {/* App routes (nested) */}
      <Route
        path="/app"
        element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<DashboardHome />} />
        <Route path="generate" element={<Generate />} />
        <Route path="history" element={<History />} />
        <Route path="analytics" element={<Analytics />} />
        <Route path="plans" element={<Plans />} />
        <Route path="brand" element={<Brand />} />
        <Route path="campaigns" element={<Campaigns />} />
      </Route>
      

      {/* Fallback */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
