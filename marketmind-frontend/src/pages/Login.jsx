import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // TEMP fake login
    console.log("Login data:", form);
    navigate("/app");
  };

  return (
    <div style={styles.wrapper}>
      <form style={styles.card} onSubmit={handleSubmit}>
        <h2>Login</h2>

        <input
          type="email"
          name="email"
          placeholder="Email"
          onChange={handleChange}
          required
          style={styles.input}
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={handleChange}
          required
          style={styles.input}
        />

        <button type="submit" style={styles.button}>
          Login
        </button>

        <p>
          No account? <Link to="/register">Register</Link>
        </p>
      </form>
    </div>
  );
}

const styles = {
 wrapper: {
        height: "100vh",
        width: "100vw",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "#0f1117",
        color: "white",
      },
  card: {
    background: "#1a1d26",
    padding: 32,
    borderRadius: 12,
    width: 350,
    display: "flex",
    flexDirection: "column",
    gap: 16,
  },
  input: {
    padding: 10,
    borderRadius: 6,
    border: "1px solid #333",
    background: "#111",
    color: "white",
  },
  button: {
    padding: 12,
    borderRadius: 6,
    border: "none",
    background: "#4f46e5",
    color: "white",
    cursor: "pointer",
  },
};
