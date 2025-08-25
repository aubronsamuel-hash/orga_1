import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import Health, { HealthView } from "./Health";

describe("HealthView presentational", () => {
  it("renders Loading", () => {
    render(<HealthView state={{ kind: "loading" }} />);
    expect(screen.getByText("Chargement...")).toBeInTheDocument();
  });
  it("renders OK", () => {
    render(<HealthView state={{ kind: "ok", body: { status: "ok", time_utc: "2025-01-01T00:00:00Z" }, requestId: "rid" }} />);
    expect(screen.getByText("OK")).toBeInTheDocument();
    expect(screen.getByText(/time_utc/)).toBeInTheDocument();
    expect(screen.getByText(/request_id/)).toBeInTheDocument();
  });
  it("renders KO", () => {
    render(<HealthView state={{ kind: "ko", status: 500 }} />);
    expect(screen.getByText(/KO/)).toBeInTheDocument();
  });
});

describe("Health integration (fetch)", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("shows OK when backend responds 200 with status ok", async () => {
    vi.spyOn(global, "fetch").mockResolvedValueOnce(new Response(JSON.stringify({ status: "ok", time_utc: "2025-01-01T00:00:00Z" }), {
      status: 200,
      headers: { "X-Request-ID": "t-1" }
    }) as unknown as Response);
    render(<Health />);
    expect(screen.getByText("Chargement...")).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText("OK")).toBeInTheDocument());
    expect(screen.getByText(/request_id: t-1/)).toBeInTheDocument();
  });

  it("shows KO when backend returns 500", async () => {
    vi.spyOn(global, "fetch").mockResolvedValueOnce(new Response("err", { status: 500 }) as unknown as Response);
    render(<Health />);
    await waitFor(() => expect(screen.getByText(/KO/)).toBeInTheDocument());
  });

  it("shows KO when fetch throws", async () => {
    vi.spyOn(global, "fetch").mockRejectedValueOnce(new Error("net"));
    render(<Health />);
    await waitFor(() => expect(screen.getByText(/KO/)).toBeInTheDocument());
  });
});

