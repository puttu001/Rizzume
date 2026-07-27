"use client";

import { useEffect, useRef, useState } from "react";

import { CameraOffIcon } from "@/features/interview/components/icons";

// Live self-view only — a mirror, nothing recorded/uploaded/stored. Pure
// getUserMedia({video: true}) + <video>, zero backend involvement.
// `enabled` toggles the existing track rather than re-requesting the
// device, so the on/off control is instant and doesn't re-prompt.
export function CameraSelfView({ enabled = true }: { enabled?: boolean }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        if (cancelled) {
          stream.getTracks().forEach((track) => track.stop());
          return;
        }
        streamRef.current = stream;
        if (videoRef.current) videoRef.current.srcObject = stream;
      })
      .catch(() => setError("Camera unavailable — check your browser permissions."));

    return () => {
      cancelled = true;
      streamRef.current?.getTracks().forEach((track) => track.stop());
    };
  }, []);

  useEffect(() => {
    streamRef.current?.getVideoTracks().forEach((track) => {
      track.enabled = enabled;
    });
  }, [enabled]);

  return (
    <div className="relative aspect-video w-full overflow-hidden rounded-2xl bg-slate-900">
      {error ? (
        <div className="flex h-full items-center justify-center px-4 text-center text-sm text-slate-400">
          {error}
        </div>
      ) : (
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          className="h-full w-full scale-x-[-1] object-cover"
        />
      )}

      {!error && !enabled && (
        <div className="absolute inset-0 flex flex-col items-center justify-center gap-2 bg-slate-900 text-slate-400">
          <CameraOffIcon className="h-6 w-6" />
          <span className="text-sm">Camera off</span>
        </div>
      )}
    </div>
  );
}