"use client";

import React from "react";
import { CheckCircle2, RefreshCw, XCircle, HelpCircle, ShieldAlert, AlertCircle } from "lucide-react";
import caseStudyData from "@/data/case-study-data.json";

export default function DecisionFrameworkSection() {
  const { decision_framework } = caseStudyData;

  const quadrantStyles: Record<string, { border: string; bg: string; text: string; icon: any }> = {
    SHIP: { border: "border-emerald-500/40", bg: "bg-emerald-950/20", text: "text-emerald-400", icon: CheckCircle2 },
    ITERATE: { border: "border-amber-500/40", bg: "bg-amber-950/20", text: "text-amber-400", icon: RefreshCw },
    ROLLBACK: { border: "border-rose-500/40", bg: "bg-rose-950/20", text: "text-rose-400", icon: XCircle },
    INCONCLUSIVE: { border: "border-slate-700", bg: "bg-slate-900/40", text: "text-slate-400", icon: HelpCircle },
  };

  return (
    <section id="decisions" className="py-20 border-b border-slate-800/60 bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="mb-10">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-2">
            <ShieldAlert className="w-4 h-4" />
            Product Governance Rules
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-white mb-2">
            Experiment Launch Decision Framework
          </h2>
          <p className="text-sm text-slate-400 max-w-2xl">
            Statistical significance is a necessary, but not sufficient, condition to ship. Rollout decisions require satisfying Statistical Rigor, Practical Significance, and Guardrail Integrity simultaneously.
          </p>
        </div>

        {/* Governance Principles Strip */}
        <div className="p-4 rounded-2xl bg-indigo-950/30 border border-indigo-800/40 mb-8 space-y-1 text-xs text-slate-300">
          <span className="font-semibold text-indigo-300 block mb-1">Core Experimentation Tenet:</span>
          <p className="text-slate-400 italic">
            "The proposed experiments are research designs. No A/B test has been executed. A statistically significant result with breached guardrails or trivial effect size will never ship."
          </p>
        </div>

        {/* 4-Quadrant Decision Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {decision_framework.quadrants.map((quad, idx) => {
            const style = quadrantStyles[quad.decision] || quadrantStyles["INCONCLUSIVE"];
            const Icon = style.icon;

            return (
              <div
                key={idx}
                className={`p-6 rounded-3xl border ${style.border} ${style.bg} flex flex-col justify-between space-y-4`}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className={`text-base font-bold font-mono ${style.text} flex items-center gap-2`}>
                      <Icon className="w-5 h-5" />
                      {quad.decision}
                    </span>
                    <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider px-2 py-0.5 rounded bg-slate-950/60 border border-slate-800">
                      Quadrant {idx + 1}
                    </span>
                  </div>

                  <div className="space-y-2 text-xs">
                    <div>
                      <span className="font-semibold text-slate-200 block mb-0.5">Decision Criteria:</span>
                      <p className="text-slate-300 leading-relaxed font-mono">{quad.criteria}</p>
                    </div>
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-800/80 text-[11px] font-mono">
                  <span className="text-slate-400 block mb-0.5">Operational Action:</span>
                  <span className="text-slate-200">{quad.action}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
