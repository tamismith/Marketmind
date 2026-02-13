import { Routes, Route, Navigate } from "react-router-dom";

import Home from "./pages/Home.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import DashboardLayout from "./layouts/DashboardLayout.jsx";
import DashboardHome from "./pages/DashboardHome.jsx";
import Generate from "./pages/Generate.jsx";


export default function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* App routes (nested) */}
      <Route path="/app" element={<DashboardLayout />}>
        <Route index element={<DashboardHome />} />
        <Route path="generate" element={<Generate />} />
      </Route>
      

      {/* Fallback */}
      <Route path="*" element={<div style={{ padding: 24 }}>404</div>} />
    </Routes>
  );
}
