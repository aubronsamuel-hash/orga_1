import { render } from "@testing-library/react";
import { axe } from "vitest-axe";
import { toHaveNoViolations } from "jest-axe";
import { describe, expect, it } from "vitest";
import { HealthView } from "./Health";

expect.extend(toHaveNoViolations);

describe("HealthView a11y", () => {
  it("has no a11y violations (OK state)", async () => {
    const { container } = render(<HealthView state={{ kind: "ok", body: { status: "ok", time_utc: "2025-01-01T00:00:00Z" } }} />);
    const result = await axe(container);
    expect(result).toHaveNoViolations();
  });
});

