import React from "react";
import { useParams } from "react-router-dom";
import { getMission } from "../lib/api_missions";
import { getTokens } from "../lib/auth";

export default function MissionDetails() {
  const { id } = useParams();
  const [m, setM] = React.useState<any | null>(null);
  const [err, setErr] = React.useState<string | null>(null);
  React.useEffect(() => {
    if (!id) return;
    const run = async () => {
      try {
        const t = getTokens();
        setM(await getMission(Number(id), t?.access));
      } catch (e: any) {
        setErr(`Erreur ${e.message}`);
      }
    };
    void run();
  }, [id]);
  if (err) return <div className="text-red-600">{err}</div>;
  if (!m) return <div>Chargement...</div>;
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">{m.title}</h1>
      <div className="text-sm">{new Date(m.start_at).toLocaleString()} - {new Date(m.end_at).toLocaleString()}</div>
      <div className="space-y-2">
        <h2 className="text-lg font-semibold">Roles</h2>
        <ul className="list-disc pl-6">
          {m.roles.map((r: any) => <li key={r.id}>{r.name} x{r.quantity}</li>)}
        </ul>
      </div>
      <div className="space-y-2">
        <h2 className="text-lg font-semibold">Assignations</h2>
        <ul className="list-disc pl-6">
          {m.assignments.map((a: any) => <li key={a.id}>user #{a.user_id} ({new Date(a.start_at).toLocaleTimeString()} - {new Date(a.end_at).toLocaleTimeString()})</li>)}
        </ul>
      </div>
    </div>
  );
}
