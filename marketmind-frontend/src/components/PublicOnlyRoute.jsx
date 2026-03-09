import { Navigate } from "react-router-dom";
import { getToken } from "../api/client";

export default function PublicOnlyRoute({ children }) {
  const token = getToken();

  if (token) {
    return <Navigate to="/app" replace />;
  }

  return children;
}
