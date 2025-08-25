export type Availability = { id: number; start_at: string; end_at: string; note?: string | null };

const BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api/v1";

export async function listAvailabilities(token?: string): Promise<Availability[]> {
  const r = await fetch(`${BASE}/availabilities`, { headers: token ? { Authorization: `Bearer ${token}` } : {} });
  if (!r.ok) throw new Error(String(r.status));
  return (await r.json()) as Availability[];
}

