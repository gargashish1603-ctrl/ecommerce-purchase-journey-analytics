"use client";

import React, { useState } from "react";
import { ArrowRight, Layers, FileText, CheckCircle2, FlaskConical, Target, Sparkles, Code2 } from "lucide-react";
import caseStudyData from "@/data/case-study-data.json";

export default function ProductTranslationSection() {
  const { traceability_sample } = caseStudyData;
  const [selectedTraceId, setSelectedTraceId] = useState<string>("PROB-01");

  const activeTrace = traceability_sample.find((t) => t.problem_id === selectedTraceId) || traceability_sample[0];

  return (
    <section id="translation" className="py-20 border-b border-slate-800/60 bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="mb-10">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-2">
            <Sparkles className="w-4 h-4" />
            From Insight to Product Execution
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-white mb-2">
            The Product Analytics Translation Engine
          </h2>
          <p className="text-sm text-slate-400 max-w-2xl">
            Demonstrating how observational clickstream evidence transforms systematically into Business Requirements, Functional Specs, User Stories, and A/B Experiments.
          </p>
        </div>

        {/* Problem Selector Strip */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-8">
          {traceability_sample.map((trace) => {
            const isSelected = trace.problem_id === selectedTraceId;
            return (
              <button
                key={trace.problem_id}
                onClick={() => setSelectedTraceId(trace.problem_id)}
                className={`p-3 rounded-xl border text-left transition-all ${
                  isSelected
                    ? "bg-indigo-950/70 border-indigo-500/60 text-white shadow-md shadow-indigo-950/40"
                    : "bg-slate-900/30 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-900/60"
                }`}
              >
                <div className="text-xs font-mono font-bold text-indigo-400 mb-0.5">{trace.problem_id}</div>
                <div className="text-xs font-semibold text-white truncate">{trace.experiment}</div>
              </button>
            );
          })}
        </div>

        {/* Translation Flow Architecture Card */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6">
          {/* Top Row: Evidence -> Problem -> Objective */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800">
              <div className="text-[11px] font-mono uppercase text-indigo-400 font-bold mb-1 flex items-center gap-1.5">
                <Target className="w-3.5 h-3.5" /> 1. Empirical Evidence
              </div>
              <div className="text-xs text-slate-200 leading-relaxed font-mono">{activeTrace.evidence}</div>
            </div>

            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800">
              <div className="text-[11px] font-mono uppercase text-violet-400 font-bold mb-1 flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5" /> 2. Product Objective
              </div>
              <div className="text-xs text-slate-200 leading-relaxed">{activeTrace.objective}</div>
            </div>

            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800">
              <div className="text-[11px] font-mono uppercase text-emerald-400 font-bold mb-1 flex items-center gap-1.5">
                <FlaskConical className="w-3.5 h-3.5" /> 3. Candidate A/B Test
              </div>
              <div className="text-xs text-slate-200 leading-relaxed font-bold">{activeTrace.experiment}</div>
              <div className="text-[11px] text-emerald-300 font-mono mt-1">KPI: {activeTrace.primary_kpi}</div>
            </div>
          </div>

          {/* Bottom Grid: BRD -> FRS -> User Story -> Acceptance Criteria */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-slate-800">
            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-slate-950/40 border border-slate-800/80">
                <span className="text-[11px] font-mono font-bold text-slate-400 uppercase block mb-1">
                  Business Requirement (BRD):
                </span>
                <p className="text-xs text-slate-300 leading-relaxed">{activeTrace.business_req}</p>
              </div>

              <div className="p-4 rounded-2xl bg-slate-950/40 border border-slate-800/80">
                <span className="text-[11px] font-mono font-bold text-slate-400 uppercase block mb-1">
                  Functional Specification (FRS):
                </span>
                <p className="text-xs text-slate-300 leading-relaxed font-mono">{activeTrace.functional_req}</p>
              </div>
            </div>

            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-slate-950/40 border border-slate-800/80">
                <span className="text-[11px] font-mono font-bold text-slate-400 uppercase block mb-1">
                  User Story (Persona):
                </span>
                <p className="text-xs text-slate-300 leading-relaxed italic">"{activeTrace.user_story}"</p>
              </div>

              <div className="p-4 rounded-2xl bg-slate-950/40 border border-slate-800/80">
                <span className="text-[11px] font-mono font-bold text-slate-400 uppercase block mb-1">
                  Given / When / Then Acceptance Criteria:
                </span>
                <p className="text-xs text-slate-300 leading-relaxed font-mono">{activeTrace.acceptance_criteria}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
