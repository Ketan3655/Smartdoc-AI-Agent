"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  getDocuments,
  uploadDocument,
  deleteDocument,
} from "../src/lib/api";
import ChatWindow from "../src/components/ChatWindow";
type Document = {
  id: string;
  filename: string;
  file_type: string;
  created_at: string;
};
import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#050816] text-white">

      {/* Navbar */}
      <nav className="border-b border-white/10">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">

          <Link
            href="/"
            className="text-xl font-bold tracking-tight"
          >
            SmartDoc <span className="text-blue-500">AI</span>
          </Link>

          <div className="flex items-center gap-4">
            <Link
              href="/login"
              className="rounded-lg px-4 py-2 text-sm text-gray-300 transition hover:bg-white/5 hover:text-white"
            >
              Login
            </Link>

            <Link
              href="/register"
              className="rounded-lg bg-blue-600 px-5 py-2 text-sm font-medium transition hover:bg-blue-500"
            >
              Get Started
            </Link>
          </div>

        </div>
      </nav>

      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute left-1/2 top-0 -z-10 h-[500px] w-[700px] -translate-x-1/2 rounded-full bg-blue-600/10 blur-[120px]" />

        <div className="mx-auto flex max-w-6xl flex-col items-center px-6 pb-24 pt-24 text-center">

          <div className="mb-6 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-2 text-sm text-blue-400">
            AI-powered document assistant
          </div>

          <h1 className="max-w-4xl text-5xl font-bold leading-tight tracking-tight md:text-7xl">
            Understand your documents
            <span className="block text-blue-500">
              with AI.
            </span>
          </h1>

          <p className="mt-7 max-w-2xl text-lg leading-8 text-gray-400">
            Upload your PDF, DOCX, or TXT documents and ask questions
            using natural language. SmartDoc AI finds the relevant
            information and gives you intelligent answers.
          </p>

          <div className="mt-10 flex flex-col gap-4 sm:flex-row">

            <Link
              href="/register"
              className="rounded-xl bg-blue-600 px-7 py-3.5 font-semibold transition hover:bg-blue-500"
            >
              Start for free →
            </Link>

            <Link
              href="/login"
              className="rounded-xl border border-white/10 bg-white/5 px-7 py-3.5 font-semibold transition hover:bg-white/10"
            >
              Sign in
            </Link>

          </div>

          <p className="mt-5 text-sm text-gray-500">
            No complicated setup. Upload a document and start asking questions.
          </p>

        </div>
      </section>

      {/* Features */}
      <section className="border-y border-white/10 bg-white/[0.02]">
        <div className="mx-auto max-w-6xl px-6 py-20">

          <div className="text-center">
            <p className="text-sm font-medium uppercase tracking-widest text-blue-500">
              Features
            </p>

            <h2 className="mt-3 text-3xl font-bold md:text-4xl">
              Everything you need to work with documents
            </h2>

            <p className="mx-auto mt-4 max-w-2xl text-gray-400">
              SmartDoc AI combines document processing, semantic search
              and AI to make your documents easier to understand.
            </p>
          </div>

          <div className="mt-14 grid gap-6 md:grid-cols-2 lg:grid-cols-4">

            <Feature
              icon="📄"
              title="Multiple formats"
              description="Upload PDF, DOCX and TXT documents."
            />

            <Feature
              icon="🔍"
              title="Smart search"
              description="Find relevant information using semantic search."
            />

            <Feature
              icon="🤖"
              title="AI answers"
              description="Ask questions and receive context-aware answers."
            />

            <Feature
              icon="🔐"
              title="Secure access"
              description="Your documents are available only to your account."
            />

          </div>

        </div>
      </section>

      {/* How it works */}
      <section className="mx-auto max-w-6xl px-6 py-24">

        <div className="text-center">

          <p className="text-sm font-medium uppercase tracking-widest text-blue-500">
            How it works
          </p>

          <h2 className="mt-3 text-3xl font-bold md:text-4xl">
            From document to answer in seconds
          </h2>

        </div>

        <div className="mt-14 grid gap-8 md:grid-cols-4">

          <Step
            number="01"
            title="Upload"
            description="Upload your PDF, DOCX or TXT document."
          />

          <Step
            number="02"
            title="Process"
            description="SmartDoc extracts and processes your document."
          />

          <Step
            number="03"
            title="Ask"
            description="Ask questions about anything inside your document."
          />

          <Step
            number="04"
            title="Answer"
            description="Get relevant AI-powered answers instantly."
          />

        </div>

      </section>

      {/* CTA */}
      <section className="px-6 pb-24">

        <div className="mx-auto max-w-5xl rounded-3xl border border-blue-500/20 bg-blue-600/10 px-6 py-16 text-center">

          <h2 className="text-3xl font-bold md:text-4xl">
            Ready to chat with your documents?
          </h2>

          <p className="mx-auto mt-4 max-w-xl text-gray-400">
            Create your account and start exploring your documents
            with SmartDoc AI.
          </p>

          <Link
            href="/register"
            className="mt-8 inline-block rounded-xl bg-blue-600 px-7 py-3.5 font-semibold transition hover:bg-blue-500"
          >
            Get Started →
          </Link>

        </div>

      </section>

      {/* Footer */}
      <footer className="border-t border-white/10">

        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-3 px-6 py-8 text-sm text-gray-500 md:flex-row">

          <p>
            © {new Date().getFullYear()} SmartDoc AI
          </p>

          <p>
            Developed by{" "}
            <span className="font-medium text-gray-300">
              Ketan Prajapati
            </span>
          </p>

        </div>

      </footer>

    </main>
  );
}


/* Feature Card */

function Feature({
  icon,
  title,
  description,
}: {
  icon: string;
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 transition hover:-translate-y-1 hover:border-blue-500/30 hover:bg-white/[0.05]">

      <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-500/10 text-2xl">
        {icon}
      </div>

      <h3 className="text-lg font-semibold">
        {title}
      </h3>

      <p className="mt-2 text-sm leading-6 text-gray-400">
        {description}
      </p>

    </div>
  );
}


/* Step */

function Step({
  number,
  title,
  description,
}: {
  number: string;
  title: string;
  description: string;
}) {
  return (
    <div className="relative">

      <div className="mb-5 text-sm font-bold text-blue-500">
        {number}
      </div>

      <h3 className="text-xl font-semibold">
        {title}
      </h3>

      <p className="mt-3 text-sm leading-6 text-gray-400">
        {description}
      </p>

    </div>
  );
}

