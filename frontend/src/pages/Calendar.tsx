import React from "react";
import { Calendar, dateFnsLocalizer, Views } from "react-big-calendar";
import "react-big-calendar/lib/css/react-big-calendar.css";
import { format, parse, startOfWeek, getDay } from "date-fns";
import { fr } from "date-fns/locale";
import { listAvailabilities } from "../lib/api_availabilities";
import { getTokens } from "../lib/auth";

const locales = { fr };
const localizer = dateFnsLocalizer({ format, parse, startOfWeek: () => startOfWeek(new Date(), { weekStartsOn: 1 }), getDay, locales });

export default function CalendarPage() {
  const [events, setEvents] = React.useState<any[]>([]);
  const [err, setErr] = React.useState<string | null>(null);

  React.useEffect(() => {
    const run = async () => {
      try {
        const t = getTokens();
        const arr = await listAvailabilities(t?.access);
        setEvents(
          arr.map(a => ({
            title: a.note || "Disponible",
            start: new Date(a.start_at),
            end: new Date(a.end_at),
            allDay: false
          }))
        );
      } catch (e: any) {
        setErr(`Erreur ${e.message}`);
      }
    };
    void run();
  }, []);

  if (err) return <div className="text-red-600">{err}</div>;

  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-bold">Calendrier</h1>
      <Calendar
        localizer={localizer}
        culture="fr"
        events={events}
        defaultView={Views.WEEK}
        startAccessor="start"
        endAccessor="end"
        style={{ height: 600 }}
      />
    </div>
  );
}

