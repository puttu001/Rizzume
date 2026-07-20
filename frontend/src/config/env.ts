import { z } from "zod";

// Fails fast at build/start time if a required var is missing, instead of
// surfacing as an obscure runtime fetch failure later.
const envSchema = z.object({
  NEXT_PUBLIC_API_URL: z.string().url(),
});

export const env = envSchema.parse({
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
});
