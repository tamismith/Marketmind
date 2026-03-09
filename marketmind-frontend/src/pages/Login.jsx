import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { api, setToken } from "../api/client";

export default function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setIsSubmitting(true);

    try {
      const data = await api.post("/auth/login", form, { auth: false });
      const token = data?.access_token;

      if (!token) {
        throw new Error("Login succeeded but no access token was returned.");
      }

      setToken(token);
      navigate("/app");
    } catch (error) {
      setErrorMessage(error.message || "Unable to login right now.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="page-center">
      <div className="card">
        <h2>Login</h2>
        <p>Welcome back — let’s generate something good.</p>

        <form className="form" onSubmit={handleSubmit}>
          <input
            className="input"
            type="email"
            name="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            required
          />

          <input
            className="input"
            type="password"
            name="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            required
          />

          <button className="btn" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Logging in..." : "Login"}
          </button>
        </form>

        {errorMessage ? (
          <p style={{ marginTop: 12, color: "#ffb4b4" }}>{errorMessage}</p>
        ) : null}

        <div className="helper-row">
          <span>No account?</span>
          <Link className="link" to="/register">
            Register
          </Link>
        </div>
      </div>
    </div>
  );
}
