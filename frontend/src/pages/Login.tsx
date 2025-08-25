import React from "react";
import { useNavigate } from "react-router-dom";
import { setTokens } from "../lib/auth";

const BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api/v1";

export default function Login() {
  const nav = useNavigate();
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [totp, setTotp] = React.useState("");
  const [err, setErr] = React.useState<string | null>(null);
  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    const r = await fetch(`${BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, totp_code: totp || undefined })
    });
    if (!r.ok) {
      setErr(`Erreur ${r.status}`);
      return;
    }
    const j = await r.json();
    setTokens({ access: j.access_token, refresh: j.refresh_token });
    nav("/profile");
  };
  return (
    <form className="max-w-sm space-y-3" onSubmit={submit}>
      <h1 className="text-2xl font-bold">Login</h1>
      <input className="w-full border p-2 rounded" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input className="w-full border p-2 rounded" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <input className="w-full border p-2 rounded" placeholder="TOTP (si active)" value={totp} onChange={e => setTotp(e.target.value)} />
      {err && <div className="text-sm text-red-600">{err}</div>}
      <button className="rounded bg-black text-white px-4 py-2">Se connecter</button>
    </form>
  );
}

