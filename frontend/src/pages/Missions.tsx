import React from "react";
import { listMissions } from "../lib/api_missions";
import { getTokens } from "../lib/auth";
import { Link } from "react-router-dom";

export default function Missions() {
  const [arr, setArr] = React.useState<any[] | null>(null);
  const [err, setErr] = React.useState<string | null>(null);
  React.useEffect(() => {
    const run = async () => {
      try {
        const t = getTokens();
        const data = await listMissions(t?.access);
        setArr(data);
      } catch (e: any) {
        setErr(`Erreur ${e.message}`);
      }
    };
    void run();
  }, []);
  if (err) return <div className="text-red-600">{err}</div>;
  if (!arr) return <div>Chargement...</div>;
  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-bold">Missions</h1>
      <ul className="space-y-2">
        {arr.map(m => (
          <li key={m.id} className="border rounded-xl p-3">
            <div className="font-semibold">{m.title}</div>
            <div className="text-sm text-gray-600">{new Date(m.start_at).toLocaleString()} - {new Date(m.end_at).toLocaleString()}</div>
            <Link to={`/missions/${m.id}`} className="text-blue-600 underline">Details</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
