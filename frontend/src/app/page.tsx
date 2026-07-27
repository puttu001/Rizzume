import Link from "next/link";

import { InterviewPreviewCard } from "@/components/InterviewPreviewCard";

const FEATURES = [
  {
    title: "Resume-aware questions",
    description:
      "Upload your resume and the interviewer opens with something grounded in your actual projects — not a generic question bank.",
  },
  {
    title: "Real voice conversation",
    description:
      "Answer out loud. Your answer is transcribed, and the next question follows naturally from what you just said.",
  },
  {
    title: "Feedback that's specific",
    description:
      "A score, concrete strengths, and areas to improve — grounded in your actual transcript, not boilerplate advice.",
  },
];

export default function LandingPage() {
  return (
    <div className="flex flex-1 flex-col">
      <section className="mx-auto flex w-full max-w-6xl flex-1 flex-col items-center gap-12 px-6 py-12 sm:px-10 lg:flex-row lg:items-center lg:py-20">
        <div className="flex max-w-xl flex-col items-start gap-6 text-left">
          <span className="rounded-full bg-indigo-100 px-3 py-1 text-xs font-semibold text-indigo-700">
            AI Interview Practice
          </span>
          <h1 className="text-4xl font-bold leading-tight tracking-tight text-slate-900 sm:text-5xl">
            Practice interviews with an AI that{" "}
            <span className="text-indigo-600">actually listens</span>.
          </h1>
          <p className="text-lg leading-8 text-slate-600">
            Upload your resume, pick a role, and have a real spoken conversation
            with an interviewer that follows up on what you actually say —
            then get honest, specific feedback when you&apos;re done.
          </p>
          <div className="flex flex-col gap-3 sm:flex-row">
            <Link
              href="/signup"
              className="rounded-full bg-indigo-600 px-6 py-3 text-center text-sm font-semibold text-white shadow-lg shadow-indigo-600/25 transition-colors hover:bg-indigo-500"
            >
              Get Started
            </Link>
            <Link
              href="/signin"
              className="rounded-full border border-slate-300 px-6 py-3 text-center text-sm font-semibold text-slate-700 transition-colors hover:bg-white"
            >
              I already have an account
            </Link>
          </div>
        </div>

        <div className="w-full max-w-md lg:flex-1">
          <InterviewPreviewCard />
        </div>
      </section>

      <section
        id="how-it-works"
        className="mx-auto w-full max-w-6xl px-6 py-16 sm:px-10"
      >
        <h2 className="text-sm font-semibold uppercase tracking-wide text-indigo-600">
          How it works
        </h2>
        <ol className="mt-4 grid gap-6 text-slate-700 sm:grid-cols-3">
          <li className="rounded-2xl border border-slate-200 bg-white/60 p-5">
            <span className="text-sm font-semibold text-indigo-600">01</span>
            <p className="mt-2 font-medium text-slate-900">Upload your resume</p>
            <p className="mt-1 text-sm text-slate-600">
              Tell it the role you&apos;re targeting.
            </p>
          </li>
          <li className="rounded-2xl border border-slate-200 bg-white/60 p-5">
            <span className="text-sm font-semibold text-indigo-600">02</span>
            <p className="mt-2 font-medium text-slate-900">Answer out loud</p>
            <p className="mt-1 text-sm text-slate-600">
              The interviewer adapts difficulty as you go.
            </p>
          </li>
          <li className="rounded-2xl border border-slate-200 bg-white/60 p-5">
            <span className="text-sm font-semibold text-indigo-600">03</span>
            <p className="mt-2 font-medium text-slate-900">Get real feedback</p>
            <p className="mt-1 text-sm text-slate-600">
              A score and specific, grounded notes.
            </p>
          </li>
        </ol>
      </section>

      <section id="features" className="mx-auto w-full max-w-6xl px-6 pb-20 sm:px-10">
        <div className="grid gap-6 sm:grid-cols-3">
          {FEATURES.map((feature) => (
            <div
              key={feature.title}
              className="rounded-2xl border border-slate-200 bg-white/60 p-6"
            >
              <p className="font-semibold text-slate-900">{feature.title}</p>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}