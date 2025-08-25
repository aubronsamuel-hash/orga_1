export type HealthBody = { status: "ok"; time_utc: string };

const BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api/v1";

export async function fetchHealth(): Promise<{
  ok: boolean;
  status: number;
  requestId?: string;
  data?: HealthBody;
}> {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 8000);
  try {
    const res = await fetch(`${BASE}/health`, {
      method: "GET",
      signal: ctrl.signal,
      headers: { "X-Request-ID": "fe-health" }
    });
    const requestId = res.headers.get("X-Request-ID") ?? undefined;
    if (!res.ok) {
      return { ok: false, status: res.status, requestId };
    }
    const json = (await res.json()) as HealthBody;
    return { ok: json.status === "ok", status: res.status, requestId, data: json };
  } catch {
    return { ok: false, status: 0 };
  } finally {
    clearTimeout(t);
  }
}

