import * as React from "react";
import { cn } from "./cn";

export function Alert({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div role="alert" className={cn("rounded-xl border border-red-300 bg-red-50 p-4 text-sm", className)} {...props} />;
}

