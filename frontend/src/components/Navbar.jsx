import React from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { LogOut, BookOpen, Sparkles, FileText, LayoutDashboard, Trophy, Compass, ShieldCheck, Bookmark, Calculator, Wand2 } from "lucide-react";

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const linkCls = ({ isActive }) =>
    `px-2 xl:px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5 xl:gap-2 ${
      isActive ? "bg-sand text-ink" : "text-muted2 hover:text-ink hover:bg-sand/60"
    }`;

  return (
    <header className="bg-paper border-b border-edge sticky top-0 z-40" data-testid="app-navbar">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        <Link to={user ? "/dashboard" : "/"} className="flex items-center gap-2 shrink-0" data-testid="nav-logo">
          <div className="w-9 h-9 rounded-xl bg-terracotta grid place-items-center text-white font-heading font-bold text-lg">
            W
          </div>
          <div className="leading-tight">
            <div className="font-heading font-bold text-ink">WAEC Elective Math AI</div>
            <div className="text-[10px] uppercase tracking-[0.2em] text-muted2">Further Maths</div>
          </div>
        </Link>

        {user ? (
          <>
            <nav className="hidden md:flex items-center gap-1 min-w-0">
              <NavLink to="/dashboard" className={linkCls} data-testid="nav-dashboard">
                <LayoutDashboard size={16} /> Dashboard
              </NavLink>
              <NavLink to="/syllabus" className={linkCls} data-testid="nav-syllabus">
                <BookOpen size={16} /> Syllabus
              </NavLink>
              <NavLink to="/topics" className={linkCls} data-testid="nav-topics">
                <Compass size={16} /> Topics
              </NavLink>
              <NavLink to="/past-questions" className={linkCls} data-testid="nav-past-questions">
                <FileText size={16} /> Past Q's
              </NavLink>
              <NavLink to="/exams" className={linkCls} data-testid="nav-exams">
                <Trophy size={16} /> Exams
              </NavLink>
              <NavLink to="/tutor" className={linkCls} data-testid="nav-tutor">
                <Sparkles size={16} /> AI Tutor
              </NavLink>
              <NavLink to="/revision" className={linkCls} data-testid="nav-revision">
                <Bookmark size={16} /> Revision
              </NavLink>
              <NavLink to="/formulas" className={linkCls} data-testid="nav-formulas">
                <Calculator size={16} /> Formulas
              </NavLink>
              <NavLink to="/playground" className={linkCls} data-testid="nav-playground">
                <Wand2 size={16} /> Solver
              </NavLink>
              {user.is_admin && (
                <NavLink to="/admin" className={linkCls} data-testid="nav-admin">
                  <ShieldCheck size={16} /> Admin
                </NavLink>
              )}
            </nav>
            <div className="flex items-center gap-3 shrink-0">
              <div className="hidden 2xl:flex flex-col items-end leading-tight">
                <span className="text-sm font-medium text-ink">{user.name}</span>
                <span className="text-xs text-muted2">{user.email}</span>
              </div>
              <button
                onClick={() => { logout(); navigate("/"); }}
                data-testid="logout-btn"
                className="p-2 rounded-lg border border-edge text-muted2 hover:text-terracotta hover:border-terracotta/40 transition-colors"
                aria-label="Log out"
              >
                <LogOut size={16} />
              </button>
            </div>
          </>
        ) : (
          <div className="flex items-center gap-2">
            <Link to="/login" data-testid="nav-login" className="btn-ghost text-sm">Log in</Link>
            <Link to="/register" data-testid="nav-register" className="btn-primary text-sm">Get started</Link>
          </div>
        )}
      </div>
    </header>
  );
};

export default Navbar;
