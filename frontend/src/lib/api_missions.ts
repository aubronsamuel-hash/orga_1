export type Mission = { id: number; title: string; location?: string | null; start_at: string; end_at: string };
export type MissionDetail = Mission & { roles: Array<{ id: number; name: string; quantity: number }>; assignments: Array<{ id: number; user_id: number }> };

const BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api/v1";

export async function listMissions(token?: string): Promise<Mission[]> {
  const r = await fetch(`${BASE}/missions`, { headers: token ? { Authorization: `Bearer ${token}` } : {} });
  if (!r.ok) throw new Error(String(r.status));
  return (await r.json()) as Mission[];
}

export async function getMission(id: number, token?: string): Promise<MissionDetail> {
  const r = await fetch(`${BASE}/missions/${id}`, { headers: token ? { Authorization: `Bearer ${token}` } : {} });
  if (!r.ok) throw new Error(String(r.status));
  return (await r.json()) as MissionDetail;
}
