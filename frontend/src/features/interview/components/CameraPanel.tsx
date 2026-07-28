"use client";

import { useState } from "react";

import { CameraIcon, CameraOffIcon } from "@/features/interview/components/icons";
import { CameraSelfView } from "@/features/interview/components/CameraSelfView";

// Rightmost column: just the candidate's own camera feed, sized to fill
// the full column height (matches the middle column's combined
// avatar + answer-controls height) rather than being capped to a
// fixed aspect ratio like it used to be.
export function CameraPanel() {
  const [cameraEnabled, setCameraEnabled] = useState(true);

  return (
    <div className="relative h-full min-h-[320px] w-full">
      <CameraSelfView enabled={cameraEnabled} />

      <span className="absolute left-3 top-3 flex items-center gap-1.5 rounded-full bg-black/50 px-3 py-1 text-xs font-medium text-white backdrop-blur">
        <span
          className={`h-1.5 w-1.5 rounded-full ${cameraEnabled ? "bg-emerald-400" : "bg-slate-400"}`}
        />
        {cameraEnabled ? "Camera On" : "Camera Off"}
      </span>

      <button
        onClick={() => setCameraEnabled((prev) => !prev)}
        className="absolute bottom-3 left-1/2 flex -translate-x-1/2 items-center gap-2 rounded-full bg-black/50 px-4 py-2 text-xs font-medium text-white backdrop-blur transition-colors hover:bg-black/70"
      >
        {cameraEnabled ? <CameraIcon className="h-4 w-4" /> : <CameraOffIcon className="h-4 w-4" />}
        {cameraEnabled ? "Turn off camera" : "Turn on camera"}
      </button>
    </div>
  );
}
