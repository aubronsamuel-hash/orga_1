import React from "react";
import { fetchHealth, type HealthBody } from "../lib/api";
import { Card, CardContent, CardHeader } from "../components/ui/card";
import { Alert } from "../components/ui/alert";
import { Spinner } from "../components/ui/spinner";
import { Button } from "../components/ui/button";

type State = { kind: "loading" } | { kind: "ok"; body: HealthBody; requestId?: string } | { kind: "ko"; status: number };

export function HealthView({ state, onRetry }: { state: State; onRetry?: () => void }) {
  if (state.kind === "loading") {
    return (
      <Card aria-busy="true" aria-live="polite">
        <CardHeader><h1 className="text-xl font-bold">Health</h1></CardHeader>
        <CardContent className="flex items-center gap-2">
          <Spinner />
          <span>Chargement...</span>
        </CardContent>
      </Card>
    );
  }
  if (state.kind === "ok") {
    return (
      <Card>
        <CardHeader><h1 className="text-xl font-bold">Health</h1></CardHeader>
        <CardContent className="space-y-2">
          <div className="text-green-700 font-semibold">OK</div>
          <div className="text-sm text-gray-600">time_utc: {state.body.time_utc}</div>
          {state.requestId && <div className="text-xs text-gray-500">request_id: {state.requestId}</div>}
        </CardContent>
      </Card>
    );
  }
  return (
    <Card>
      <CardHeader><h1 className="text-xl font-bold">Health</h1></CardHeader>
      <CardContent className="space-y-3">
        <Alert>KO (status {state.status || 0}). Verifiez que le backend tourne.</Alert>
        {onRetry && <Button onClick={onRetry} variant="default">Reessayer</Button>}
      </CardContent>
    </Card>
  );
}

export default function Health() {
  const [state, setState] = React.useState<State>({ kind: "loading" });

  const run = React.useCallback(async () => {
    setState({ kind: "loading" });
    const r = await fetchHealth();
    if (r.ok && r.data) {
      setState({ kind: "ok", body: r.data, requestId: r.requestId });
    } else {
      setState({ kind: "ko", status: r.status });
    }
  }, []);

  React.useEffect(() => { void run(); }, [run]);

  return <HealthView state={state} onRetry={run} />;
}

