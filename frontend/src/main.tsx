import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import Health from "./pages/Health";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import { getTokens } from "./lib/auth";
import "./index.css";

function Nav() {
  const authed = !!getTokens();
  return (
    <nav className="w-full border-b border-border">
      <div className="max-w-5xl mx-auto p-4 flex gap-4">
        <Link to="/">Accueil</Link>
        <Link to="/health">Health</Link>
        {!authed && <Link to="/login">Login</Link>}
        {!authed && <Link to="/register">Register</Link>}
        {authed && <Link to="/profile">Profil</Link>}
      </div>
    </nav>
  );
}

function RequireAuth({ children }: { children: React.ReactNode }) {
  return getTokens() ? <>{children}</> : <Navigate to="/login" replace />;
}

function Shell() {
  return (
    <BrowserRouter>
      <Nav />
      <main className="max-w-5xl mx-auto p-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/health" element={<Health />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/profile" element={<RequireAuth><Profile /></RequireAuth>} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Shell />
  </React.StrictMode>
);

