export type Tokens = { access: string; refresh: string };

let memory: Tokens | null = null;

export function setTokens(t: Tokens | null) {
  memory = t;
  if (t) {
    sessionStorage.setItem("cc_tokens", JSON.stringify(t));
  } else {
    sessionStorage.removeItem("cc_tokens");
  }
}

export function getTokens(): Tokens | null {
  if (memory) return memory;
  const raw = sessionStorage.getItem("cc_tokens");
  if (!raw) return null;
  try {
    memory = JSON.parse(raw) as Tokens;
    return memory;
  } catch {
    return null;
  }
}

export function authHeader(): HeadersInit {
  const t = getTokens();
  return t ? { Authorization: `Bearer ${t.access}` } : {};
}

