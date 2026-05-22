import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { toast } from "sonner";

const Login = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("student@waec.com");
  const [password, setPassword] = useState("Student@123");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(email, password);
      toast.success("Welcome back!");
      navigate("/dashboard");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] grid place-items-center px-4 py-12" data-testid="login-page">
      <div className="w-full max-w-md card-surface p-8">
        <span className="overline">Sign in</span>
        <h1 className="font-heading mt-2 text-3xl font-semibold text-ink">Welcome back</h1>
        <p className="text-muted2 mt-1 text-sm">Continue your WAEC math journey.</p>
        <form onSubmit={submit} className="mt-6 space-y-4">
          <div>
            <label className="text-sm font-medium text-ink">Email</label>
            <input
              type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
              data-testid="login-email-input"
              className="mt-1 w-full px-4 py-3 rounded-xl border border-edge bg-surface focus:outline-none focus:ring-2 focus:ring-terracotta/40 focus:border-terracotta transition"
            />
          </div>
          <div>
            <label className="text-sm font-medium text-ink">Password</label>
            <input
              type="password" required value={password} onChange={(e) => setPassword(e.target.value)}
              data-testid="login-password-input"
              className="mt-1 w-full px-4 py-3 rounded-xl border border-edge bg-surface focus:outline-none focus:ring-2 focus:ring-terracotta/40 focus:border-terracotta transition"
            />
          </div>
          <button type="submit" disabled={loading} data-testid="login-submit-btn" className="btn-primary w-full disabled:opacity-60">
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>
        <p className="mt-5 text-sm text-muted2 text-center">
          New here?{" "}
          <Link to="/register" className="text-terracotta font-medium hover:underline" data-testid="register-link">
            Create an account
          </Link>
        </p>
        <p className="mt-3 text-xs text-muted2 text-center">
          Demo: <span className="font-mono">student@waec.com</span> / <span className="font-mono">Student@123</span>
        </p>
      </div>
    </div>
  );
};

export default Login;
