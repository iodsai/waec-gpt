import React from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "sonner";

import { AuthProvider, useAuth } from "@/context/AuthContext";
import Navbar from "@/components/Navbar";
import ProtectedRoute from "@/components/ProtectedRoute";

import Landing from "@/pages/Landing";
import Login from "@/pages/Login";
import Register from "@/pages/Register";
import Dashboard from "@/pages/Dashboard";
import Topics from "@/pages/Topics";
import TopicDetail from "@/pages/TopicDetail";
import Lessons from "@/pages/Lessons";
import PastQuestions from "@/pages/PastQuestions";
import Tutor from "@/pages/Tutor";
import Exams from "@/pages/Exams";
import ExamRun from "@/pages/ExamRun";
import ExamReport from "@/pages/ExamReport";
import Admin from "@/pages/Admin";
import RevisionDeck from "@/pages/RevisionDeck";

const LandingRoute = () => {
  const { user, loading } = useAuth();
  if (loading) return <div className="p-10 text-muted2">Loading…</div>;
  return user ? <Navigate to="/dashboard" replace /> : <Landing />;
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="app-shell">
          <Navbar />
          <Routes>
            <Route path="/" element={<LandingRoute />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/topics" element={<ProtectedRoute><Topics /></ProtectedRoute>} />
            <Route path="/topics/:topicId" element={<ProtectedRoute><TopicDetail /></ProtectedRoute>} />
            <Route path="/lessons" element={<ProtectedRoute><Lessons /></ProtectedRoute>} />
            <Route path="/lessons/:subtopicId" element={<ProtectedRoute><Lessons /></ProtectedRoute>} />
            <Route path="/past-questions" element={<ProtectedRoute><PastQuestions /></ProtectedRoute>} />
            <Route path="/tutor" element={<ProtectedRoute><Tutor /></ProtectedRoute>} />
            <Route path="/exams" element={<ProtectedRoute><Exams /></ProtectedRoute>} />
            <Route path="/exams/:examId/run" element={<ProtectedRoute><ExamRun /></ProtectedRoute>} />
            <Route path="/exams/:examId/report" element={<ProtectedRoute><ExamReport /></ProtectedRoute>} />
            <Route path="/admin" element={<ProtectedRoute><Admin /></ProtectedRoute>} />
            <Route path="/revision" element={<ProtectedRoute><RevisionDeck /></ProtectedRoute>} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
          <Toaster position="bottom-right" richColors closeButton offset={20} />
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
