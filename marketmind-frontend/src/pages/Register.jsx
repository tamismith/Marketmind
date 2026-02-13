import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Register data:", form);

    // TEMP fake register
    navigate("/login");
  };

  return (
    <div className="page-center">
      <div className="card">
        <h2>Create account</h2>
        <p>Set up your MarketMind profile in seconds.</p>

        <form className="form" onSubmit={handleSubmit}>
          <input
            className="input"
            name="name"
            placeholder="Full name"
            value={form.name}
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

          <button className="btn" type="submit">
            Create account
          </button>
        </form>

        <div className="helper-row">
          <span>Already have an account?</span>
          <Link className="link" to="/login">
            Login
          </Link>
        </div>
      </div>
    </div>
  );
}
