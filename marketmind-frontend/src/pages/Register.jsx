import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { api, setToken } from "../api/client";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ business_name: "", email: "", password: "" });
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
      await api.post(
        "/auth/register",
        {
          email: form.email,
          password: form.password,
          business_name: form.business_name,
        },
        { auth: false },
      );

      const loginData = await api.post(
        "/auth/login",
        {
          email: form.email,
          password: form.password,
        },
        { auth: false },
      );
      const token = loginData?.access_token;
      if (!token) {
        throw new Error("Registered, but could not sign in automatically.");
      }

      setToken(token);
      navigate("/app");
    } catch (error) {
      setErrorMessage(error.message || "Unable to register right now.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="page-center">
      <div className="card">
        <h2>Create account</h2>
        <p>Set up your MarketMind profile in seconds.</p>

        <form className="form" onSubmit={handleSubmit}>
          <input
            className="input"
            name="business_name"
            placeholder="Business name"
            value={form.business_name}
            onChange={handleChange}
            required
          />

          <input
            className="input"
            name="email"
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            required
          />

          <input
            className="input"
            name="password"
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            required
          />

          <button className="btn" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Creating account..." : "Create account"}
          </button>
        </form>

        {errorMessage ? (
          <p style={{ marginTop: 12, color: "#ffb4b4" }}>{errorMessage}</p>
        ) : null}

        <div className="helper-row">
          <Link className="link" to="/">
            Back to Home
          </Link>
          <span>•</span>
          <span>Already have an account?</span>
          <Link className="link" to="/login">
            Login
          </Link>
        </div>
      </div>
    </div>
  );
}
