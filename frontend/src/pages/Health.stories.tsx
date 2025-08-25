import type { Meta, StoryObj } from "@storybook/react";
import { HealthView } from "./Health";

const meta: Meta<typeof HealthView> = {
  title: "Pages/Health",
  component: HealthView
};
export default meta;

type S = StoryObj<typeof HealthView>;

export const Loading: S = { args: { state: { kind: "loading" } } };
export const Ok: S = { args: { state: { kind: "ok", body: { status: "ok", time_utc: "2025-01-01T00:00:00Z" }, requestId: "storybook" } } };
export const Ko: S = { args: { state: { kind: "ko", status: 500 } } };

