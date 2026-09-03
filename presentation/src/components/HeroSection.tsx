"use client";

import React from "react";
import { ArrowDown, AlertCircle, CheckCircle2, Search, Compass, Target, FlaskConical, BarChart3 } from "lucide-react";
import caseStudyData from "@/data/case-study-data.json";

export default function HeroSection() {
  const { headline_metrics, methodology_tagline, disclaimer } = caseStudyData;

  return (
    <section id="overview" className="relative pt-32 pb-20 overflow-hidden border-b border-slate-800/60">
      {/* Background ambient lighting */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[500px] pointer-events-none opacity-25">
        <div className="absolute top-12 left-1/4 w-96 h-96 bg-indigo-600/30 rounded-full blur-3xl" />
        <div className="absolute top-20 right-1/4 w-96 h-96 bg-violet-600/20 rounded-full blur-3xl" />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Context Pill */}
        <div className="flex flex-wrap items-center gap-2 mb-6">
          <span className="inline-flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-indigo-400 bg-indigo-950/60 border border-indigo-800/60 px-3 py-1 rounded-full">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
            ShopSphere Case Study
          </span>
          <span className="text-xs text-slate-400 font-mono">Role: Product Analyst / Business Analyst</span>
        </div>

        {/* Headline */}
        <div className="max-w-4xl">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-white leading-tight mb-4">
            Why Do Customers <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-violet-400 to-pink-400">Abandon Their Purchases?</span>
          </h1>
          <p className="text-lg sm:text-xl text-slate-300 font-medium mb-4">
            A data-driven investigation of the e-commerce purchase journey
          </p>
          <p className="text-sm sm:text-base text-slate-400 leading-relaxed max-w-3xl mb-8">
            I reconstructed the full customer purchase journey from session-level clickstream event data, investigated where friction concentrates, diagnosed statistical root causes, and translated empirical findings into testable product requirements and A/B experiments.
          </p>
        </div>

        {/* Methodology Pathway */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-3.5 mb-10 inline-flex flex-wrap items-center gap-2 sm:gap-4 text-xs font-mono text-slate-300">
          <span className="text-slate-400 font-semibold uppercase tracking-wider text-[11px]">Methodology:</span>
          <span className="flex items-center gap-1 text-indigo-300 font-medium"><Search className="w-3.5 h-3.5 text-indigo-400" /> Observe</span>
          <span className="text-slate-600">→</span>
          <span className="flex items-center gap-1 text-violet-300 font-medium"><Compass className="w-3.5 h-3.5 text-violet-400" /> Investigate</span>
          <span className="text-slate-600">→</span>
          <span className="flex items-center gap-1 text-amber-300 font-medium"><Target className="w-3.5 h-3.5 text-amber-400" /> Diagnose</span>
          <span className="text-slate-600">→</span>
          <span className="flex items-center gap-1 text-emerald-300 font-medium"><BarChart3 className="w-3.5 h-3.5 text-emerald-400" /> Define</span>
          <span className="text-slate-600">→</span>
          <span className="flex items-center gap-1 text-cyan-300 font-medium"><FlaskConical className="w-3.5 h-3.5 text-cyan-400" /> Experiment</span>
        </div>

        {/* Headline Metrics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 sm:gap-4 mb-8">
          {headline_metrics.map((metric, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-xl border transition-all ${
                metric.highlight
                  ? "bg-gradient-to-b from-indigo-950/70 to-slate-900/80 border-indigo-500/40 shadow-lg shadow-indigo-950/30"
                  : "bg-slate-900/40 border-slate-800/80 hover:border-slate-700"
              }`}
            >
              <div className="text-2xl sm:text-3xl font-bold font-mono tracking-tight text-white mb-1">
                {metric.value}
              </div>
              <div className="text-xs font-semibold text-slate-200 mb-1">{metric.label}</div>
              <div className="text-[11px] text-slate-400 leading-snug">{metric.description}</div>
            </div>
          ))}
        </div>

        {/* Synthetic Data Disclaimer Banner */}
        <div className="flex items-start gap-3 p-3.5 rounded-xl bg-slate-900/40 border border-slate-800/80 text-xs text-slate-400">
          <AlertCircle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold text-slate-300">Methodological Transparency Notice: </span>
            {disclaimer}
          </div>
        </div>
      </div>
    </section>
  );
}
