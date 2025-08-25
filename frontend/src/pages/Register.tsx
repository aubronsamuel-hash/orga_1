import React from "react";

const BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api/v1";

export default function Register() {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [msg, setMsg] = React.useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMsg(null);
    const r = await fetch(`${BASE}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    setMsg(r.ok ? "Compte cree" : `Erreur ${r.status}`);
  };

  return (
    <form className="max-w-sm space-y-3" onSubmit={submit}>
      <h1 className="text-2xl font-bold">Register</h1>
      <input className="w-full border p-2 rounded" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input className="w-full border p-2 rounded" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      {msg && <div className="text-sm">{msg}</div>}
      <button className="rounded bg-black text-white px-4 py-2">Creer</button>
    </form>
  );
}

