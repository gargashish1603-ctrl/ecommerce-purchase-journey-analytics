"use client";

import React, { useState } from "react";
import { Target, AlertTriangle, ShieldCheck, ArrowRight, ExternalLink } from "lucide-react";
import caseStudyData from "@/data/case-study-data.json";

export default function RootCausePrioritySection() {
  const { prioritized_problems } = caseStudyData;
  const [activeFilter, setActiveFilter] = useState<string>("ALL");

  const filteredProblems = activeFilter === "ALL"
    ? prioritized_problems
    : prioritized_problems.filter((p) => p.priority.startsWith(activeFilter));

  return (
    <section id="priorities" className="py-20 border-b border-slate-800/60 bg-slate-950/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-2">
              <Target className="w-4 h-4" />
              Prioritized Product Diagnosis
            </div>
            <h2 className="text-3xl font-bold tracking-tight text-white mb-2">
              Root-Cause Prioritization Matrix
            </h2>
            <p className="text-sm text-slate-400 max-w-2xl">
              Ranked using a multi-criteria scoring model weighting statistical evidence strength, customer intent, volume impact, and engineering intervenability.
            </p>
          </div>

          {/* Filter Buttons */}
          <div className="flex items-center bg-slate-900 border border-slate-800 p-1 rounded-xl">
            {["ALL", "P0", "P1", "P2"].map((tier) => (
              <button
                key={tier}
                onClick={() => setActiveFilter(tier)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  activeFilter === tier
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                {tier === "ALL" ? "All Priorities (6)" : `${tier} Tier`}
              </button>
            ))}
          </div>
        </div>

        {/* Priority Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredProblems.map((prob) => {
            const isP0 = prob.priority.startsWith("P0");
            const isP1 = prob.priority.startsWith("P1");

            return (
              <div
                key={prob.id}
                className={`p-5 rounded-2xl border transition-all flex flex-col justify-between ${
                  isP0
                    ? "bg-slate-900/60 border-rose-500/30 hover:border-rose-500/60 shadow-lg shadow-rose-950/20"
                    : isP1
                    ? "bg-slate-900/40 border-amber-500/30 hover:border-amber-500/60"
                    : "bg-slate-900/20 border-slate-800 hover:border-slate-700"
                }`}
              >
                <div>
                  {/* Card Header */}
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-indigo-300">
                        {prob.id}
                      </span>
                      <span
                        className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border ${
                          isP0
                            ? "bg-rose-950/60 text-rose-300 border-rose-800/60"
                            : isP1
                            ? "bg-amber-950/60 text-amber-300 border-amber-800/60"
                            : "bg-slate-800 text-slate-300 border-slate-700"
                        }`}
                      >
                        {prob.priority}
                      </span>
                    </div>
                    <span className="text-xs font-mono font-bold text-slate-300">
                      Rank #{prob.rank} ({prob.score})
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-white mb-1.5 leading-snug">{prob.title}</h3>
                  <div className="text-[11px] font-mono text-indigo-400 mb-3">{prob.stage}</div>

                  {/* Evidence Text */}
                  <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80 mb-3 text-xs text-slate-300 leading-relaxed">
                    <span className="font-semibold text-slate-200 block mb-1">Audited Evidence:</span>
                    {prob.evidence_summary}
                  </div>

                  {/* Candidate Intervention */}
                  <div className="text-xs text-slate-400 mb-3">
                    <span className="font-semibold text-slate-300 block mb-0.5">Candidate Intervention:</span>
                    {prob.candidate_intervention}
                  </div>
                </div>

                {/* Footer Tag */}
                <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono">
                  <span className="text-slate-400">Target Test:</span>
                  <span className="text-emerald-400 font-semibold">{prob.experiment_id}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
