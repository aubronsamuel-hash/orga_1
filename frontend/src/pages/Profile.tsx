import React from "react";
import { authHeader, getTokens, setTokens } from "../lib/auth";

const BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api/v1";

type Me = { email: string; is_admin: boolean; totp_enabled: boolean };

export default function Profile() {
  const [me, setMe] = React.useState<Me | null>(null);
  const [err, setErr] = React.useState<string | null>(null);

  React.useEffect(() => {
    const run = async () => {
      const r = await fetch(`${BASE}/users/me`, { headers: authHeader() });
      if (!r.ok) {
        setErr(`Erreur ${r.status}`);
        return;
      }
      setMe((await r.json()) as Me);
    };
    void run();
  }, []);

  const logout = async () => {
    const t = getTokens();
    if (t) {
      await fetch(`${BASE}/auth/logout?refresh_token=${encodeURIComponent(t.refresh)}`, { method: "POST" });
    }
    setTokens(null);
    location.href = "/";
  };

  if (err) return <div className="text-red-600">{err}</div>;
  if (!me) return <div>Chargement...</div>;
  return (
    <div className="space-y-2">
      <h1 className="text-2xl font-bold">Profil</h1>
      <div>Email: {me.email}</div>
      <div>Admin: {String(me.is_admin)}</div>
      <div>2FA active: {String(me.totp_enabled)}</div>
      <button className="rounded bg-black text-white px-4 py-2" onClick={logout}>Se deconnecter</button>
    </div>
  );
}

