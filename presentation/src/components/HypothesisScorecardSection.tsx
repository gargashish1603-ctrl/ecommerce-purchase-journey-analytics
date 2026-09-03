"use client";

import React, { useState } from "react";
import { CheckCircle2, XCircle, AlertCircle, HelpCircle, Layers, Filter } from "lucide-react";
import caseStudyData from "@/data/case-study-data.json";

export default function HypothesisScorecardSection() {
  const { hypothesis_scorecard } = caseStudyData;
  const [filter, setFilter] = useState<string>("ALL");

  const filteredHypotheses = hypothesis_scorecard.filter((h) => {
    if (filter === "ALL") return true;
    if (filter === "SUPPORTED") return h.verdict.startsWith("Supported");
    if (filter === "NOT_SUPPORTED") return h.verdict.startsWith("Not Supported");
    return true;
  });

  return (
    <section id="hypotheses" className="py-20 border-b border-slate-800/60 bg-slate-950/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-2">
              <Layers className="w-4 h-4" />
              Empirical Evaluation Framework
            </div>
            <h2 className="text-3xl font-bold tracking-tight text-white mb-2">
              Hypothesis Scorecard (H1–H10)
            </h2>
            <p className="text-sm text-slate-400 max-w-2xl">
              10 pre-registered analytical hypotheses evaluated using multivariate regression, non-parametric tests, and confounding controls.
            </p>
          </div>

          {/* Filter Pills */}
          <div className="flex items-center gap-1.5 p-1 bg-slate-900 border border-slate-800 rounded-xl">
            <button
              onClick={() => setFilter("ALL")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                filter === "ALL" ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30" : "text-slate-400 hover:text-white"
              }`}
            >
              All (10)
            </button>
            <button
              onClick={() => setFilter("SUPPORTED")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                filter === "SUPPORTED" ? "bg-emerald-600 text-white shadow-md shadow-emerald-600/30" : "text-slate-400 hover:text-white"
              }`}
            >
              Supported (8)
            </button>
            <button
              onClick={() => setFilter("NOT_SUPPORTED")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                filter === "NOT_SUPPORTED" ? "bg-rose-600 text-white shadow-md shadow-rose-600/30" : "text-slate-400 hover:text-white"
              }`}
            >
              Not Supported (2)
            </button>
          </div>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap items-center gap-4 mb-6 text-xs text-slate-400 px-1">
          <span className="font-semibold text-slate-300">Verdict Legend:</span>
          <span className="inline-flex items-center gap-1 text-emerald-400">
            <CheckCircle2 className="w-3.5 h-3.5" /> Supported by Data
          </span>
          <span className="inline-flex items-center gap-1 text-rose-400">
            <XCircle className="w-3.5 h-3.5" /> Not Supported / Confounded
          </span>
          <span className="inline-flex items-center gap-1 text-amber-400">
            <AlertCircle className="w-3.5 h-3.5" /> Observational / Selection Bias
          </span>
        </div>

        {/* Hypothesis Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredHypotheses.map((h) => {
            const isSupported = h.verdict.startsWith("Supported");
            const isConfounded = h.id === "H2" || h.id === "H7";

            return (
              <div
                key={h.id}
                className={`p-5 rounded-2xl border transition-all flex flex-col justify-between ${
                  isSupported
                    ? "bg-slate-900/40 border-slate-800 hover:border-slate-700"
                    : "bg-rose-950/10 border-rose-900/40 hover:border-rose-800/60"
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-indigo-300">
                      {h.id}
                    </span>
                    <span
                      className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full border inline-flex items-center gap-1 ${
                        isSupported
                          ? "bg-emerald-950/60 text-emerald-300 border-emerald-800/60"
                          : "bg-rose-950/60 text-rose-300 border-rose-800/60"
                      }`}
                    >
                      {isSupported ? <CheckCircle2 className="w-3 h-3" /> : <XCircle className="w-3 h-3" />}
                      {h.verdict}
                    </span>
                  </div>

                  <h3 className="text-sm font-bold text-white mb-1.5">{h.title}</h3>
                  <p className="text-xs text-slate-300 italic mb-3 font-mono">"{h.statement}"</p>

                  {/* Empirical Evidence */}
                  <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80 mb-3 text-xs text-slate-300 leading-relaxed">
                    <span className="font-semibold text-slate-200 block mb-1">Empirical Evidence:</span>
                    {h.evidence}
                  </div>
                </div>

                {/* Caveat */}
                <div className="pt-2.5 border-t border-slate-800/80 text-[11px] text-amber-300/90 leading-snug flex items-start gap-1.5">
                  <AlertCircle className="w-3.5 h-3.5 shrink-0 text-amber-400 mt-0.5" />
                  <span>
                    <strong className="text-slate-200">Caveat:</strong> {h.caveat}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
