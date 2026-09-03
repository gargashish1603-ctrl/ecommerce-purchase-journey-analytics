"use client";

import React from "react";
import { AlertCircle, HelpCircle, Eye, MessageSquare, ClipboardList, Shield } from "lucide-react";
import caseStudyData from "@/data/case-study-data.json";

export default function ResearchGapsSection() {
  const { research_gaps } = caseStudyData;

  return (
    <section id="gaps" className="py-20 border-b border-slate-800/60 bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="mb-10">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-amber-400 mb-2">
            <HelpCircle className="w-4 h-4" />
            Methodological Boundaries & Integrity
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-white mb-2">
            What the Clickstream Data Cannot Tell Us
          </h2>
          <p className="text-sm text-slate-400 max-w-2xl">
            Observational event logs record what users did, not what they thought. Explicitly documenting what requires qualitative user research before capital expenditure.
          </p>
        </div>

        {/* Limitations Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
          {research_gaps.map((gap, idx) => (
            <div
              key={idx}
              className="p-5 rounded-2xl bg-slate-900/40 border border-slate-800 flex flex-col justify-between space-y-4"
            >
              <div>
                <div className="flex items-center gap-2 text-xs font-mono font-bold text-amber-400 mb-2">
                  <AlertCircle className="w-4 h-4 shrink-0" />
                  {gap.gap}
                </div>
                <p className="text-xs text-slate-300 leading-relaxed mb-3">{gap.limitation}</p>
              </div>

              <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800/80 text-[11px] font-mono text-indigo-300">
                <span className="text-slate-400 block mb-0.5 font-bold uppercase text-[10px]">
                  Proposed Research Protocol:
                </span>
                {gap.protocol}
              </div>
            </div>
          ))}
        </div>

        {/* Analytical Transparency Card */}
        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 space-y-2">
          <span className="font-semibold text-white block">Analytical Transparency Summary:</span>
          <p className="leading-relaxed">
            This investigation intentionally did NOT fabricate user interviews, customer quotes, or post-launch A/B test results. All conversion baselines and sample sizes represent pre-experiment planning models grounded in audited synthetic clickstream event logs.
          </p>
        </div>
      </div>
    </section>
  );
}
