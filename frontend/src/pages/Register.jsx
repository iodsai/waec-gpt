import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { toast } from "sonner";

const Register = () => {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    if (password.length < 6) {
      toast.error("Password must be at least 6 characters.");
      return;
    }
    setLoading(true);
    try {
      await register(name, email, password);
      toast.success("Account created. Welcome!");
      navigate("/dashboard");
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] grid place-items-center px-4 py-12" data-testid="register-page">
      <div className="w-full max-w-md card-surface p-8">
        <span className="overline">Get started</span>
        <h1 className="font-heading mt-2 text-3xl font-semibold text-ink">Create your account</h1>
        <p className="text-muted2 mt-1 text-sm">Free for WAEC students. No credit card needed.</p>
        <form onSubmit={submit} className="mt-6 space-y-4">
          <div>
            <label className="text-sm font-medium text-ink">Full name</label>
            <input
              required value={name} onChange={(e) => setName(e.target.value)}
              data-testid="register-name-input"
              className="mt-1 w-full px-4 py-3 rounded-xl border border-edge bg-surface focus:outline-none focus:ring-2 focus:ring-terracotta/40 focus:border-terracotta transition"
            />
          </div>
          <div>
            <label className="text-sm font-medium text-ink">Email</label>
            <input
              type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
              data-testid="register-email-input"
              className="mt-1 w-full px-4 py-3 rounded-xl border border-edge bg-surface focus:outline-none focus:ring-2 focus:ring-terracotta/40 focus:border-terracotta transition"
            />
          </div>
          <div>
            <label className="text-sm font-medium text-ink">Password</label>
            <input
              type="password" required value={password} onChange={(e) => setPassword(e.target.value)}
              data-testid="register-password-input"
              className="mt-1 w-full px-4 py-3 rounded-xl border border-edge bg-surface focus:outline-none focus:ring-2 focus:ring-terracotta/40 focus:border-terracotta transition"
            />
          </div>
          <button type="submit" disabled={loading} data-testid="register-submit-btn" className="btn-primary w-full disabled:opacity-60">
            {loading ? "Creating…" : "Create account"}
          </button>
        </form>
        <p className="mt-5 text-sm text-muted2 text-center">
          Already have an account?{" "}
          <Link to="/login" className="text-terracotta font-medium hover:underline" data-testid="login-link">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
