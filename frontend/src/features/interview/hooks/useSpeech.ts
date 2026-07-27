"use client";

import { useCallback, useRef, useState } from "react";

import { synthesizeSpeech } from "@/features/audio/api";

// Drives the avatar's "speaking" indicator off real TTS audio playback —
// not a lip-synced character, just isSpeaking synced to an <audio> element
// (see the avatar-complexity decision).
export function useSpeech() {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const speak = useCallback(async (text: string) => {
    const blob = await synthesizeSpeech(text);
    const url = URL.createObjectURL(blob);

    // Stop whatever's currently playing right before swapping it out — a
    // real bug reproduced via React StrictMode's dev-only double effect
    // invocation played two overlapping TTS calls on mount.
    audioRef.current?.pause();

    const audio = new Audio(url);
    audioRef.current = audio;

    audio.onplay = () => setIsSpeaking(true);
    audio.onended = () => {
      setIsSpeaking(false);
      URL.revokeObjectURL(url);
    };
    audio.onerror = () => {
      setIsSpeaking(false);
      URL.revokeObjectURL(url);
    };

    await audio.play();
  }, []);

  const stop = useCallback(() => {
    audioRef.current?.pause();
    setIsSpeaking(false);
  }, []);

  return { isSpeaking, speak, stop };
}