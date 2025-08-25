import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Health from "./pages/Health";
import "./index.css";

function Nav() {
  return (
    <nav className="w-full border-b border-border">
      <div className="max-w-5xl mx-auto p-4 flex gap-4">
        <Link to="/">Accueil</Link>
        <Link to="/health">Health</Link>
      </div>
    </nav>
  );
}

function Shell() {
  return (
    <BrowserRouter>
      <Nav />
      <main className="max-w-5xl mx-auto p-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/health" element={<Health />} />
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

