"use client";

import React, { useState } from "react";
import { FlaskConical, Clock, Users, Target, Shield, CheckCircle2, ChevronDown, ChevronUp, AlertCircle } from "lucide-react";
import caseStudyData from "@/data/case-study-data.json";

export default function ExperimentPortfolioSection() {
  const { experiments } = caseStudyData;
  const [expandedExpId, setExpandedExpId] = useState<string | null>("EXP-01");

  const toggleExpand = (id: string) => {
    setExpandedExpId(expandedExpId === id ? null : id);
  };

  return (
    <section id="experiments" className="py-20 border-b border-slate-800/60 bg-slate-950/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="mb-10">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-2">
            <FlaskConical className="w-4 h-4" />
            A/B Testing Architecture
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-white mb-2">
            The Experimentation Portfolio
          </h2>
          <p className="text-sm text-slate-400 max-w-2xl">
            Candidate A/B test designs complete with falsifiable hypotheses, primary KPI formulations, statistical power calculations, runtime planning, and launch decision rules.
          </p>
        </div>

        {/* Experiment Cards Grid */}
        <div className="space-y-6">
          {experiments.map((exp) => {
            const isExpanded = expandedExpId === exp.id;

            return (
              <div
                key={exp.id}
                className="bg-slate-900/50 border border-slate-800 rounded-3xl p-6 sm:p-8 transition-all hover:border-slate-700"
              >
                {/* Header Row */}
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-6 border-b border-slate-800">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2.5">
                      <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800/60">
                        {exp.id}
                      </span>
                      <span className="text-xs font-mono text-slate-400">{exp.target_stage}</span>
                    </div>
                    <h3 className="text-xl font-bold text-white">{exp.name}</h3>
                  </div>

                  {/* High-level Runtime & Power Badge */}
                  <div className="flex flex-wrap items-center gap-3">
                    <div className="px-3 py-1.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs font-mono">
                      <span className="text-slate-400">Runtime: </span>
                      <span className="text-amber-300 font-bold">{exp.runtime}</span>
                    </div>
                    <div className="px-3 py-1.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs font-mono">
                      <span className="text-slate-400">Total Sample: </span>
                      <span className="text-emerald-300 font-bold">{exp.total_sample}</span>
                    </div>
                    <button
                      onClick={() => toggleExpand(exp.id)}
                      className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
                      aria-label="Toggle experiment details"
                    >
                      {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* Primary Hypothesis & KPI Strip */}
                <div className="grid grid-cols-1 md:grid-cols-12 gap-6 my-6">
                  {/* Hypothesis */}
                  <div className="md:col-span-7 p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-2">
                    <span className="text-[11px] font-mono uppercase font-bold text-indigo-400 block">
                      Testable Hypothesis:
                    </span>
                    <p className="text-xs text-slate-300 italic leading-relaxed">"{exp.hypothesis}"</p>
                  </div>

                  {/* Primary Metric Metrics Card */}
                  <div className="md:col-span-5 p-4 rounded-2xl bg-indigo-950/30 border border-indigo-800/40 space-y-2">
                    <span className="text-[11px] font-mono uppercase font-bold text-emerald-400 block">
                      Primary Success Metric:
                    </span>
                    <div className="text-sm font-bold text-white">{exp.primary_metric}</div>
                    <div className="flex items-center justify-between text-xs font-mono pt-1 border-t border-indigo-800/30">
                      <span className="text-slate-400">Baseline: <strong className="text-slate-200">{exp.baseline}</strong></span>
                      <span className="text-emerald-400 font-semibold">Target MDE: {exp.mde}</span>
                    </div>
                  </div>
                </div>

                {/* Expandable Deep-Dive Details */}
                {isExpanded && (
                  <div className="pt-6 border-t border-slate-800 space-y-6 animate-fadeIn">
                    {/* Control vs Treatment */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div className="p-4 rounded-2xl bg-slate-950/40 border border-slate-800">
                        <span className="text-[11px] font-mono font-bold text-slate-400 uppercase block mb-1">
                          Control Variant (A):
                        </span>
                        <p className="text-xs text-slate-300">{exp.control}</p>
                      </div>

                      <div className="p-4 rounded-2xl bg-slate-950/40 border border-slate-800">
                        <span className="text-[11px] font-mono font-bold text-indigo-400 uppercase block mb-1">
                          Treatment Variant (B):
                        </span>
                        <p className="text-xs text-slate-300">{exp.treatment}</p>
                      </div>
                    </div>

                    {/* Secondary Metrics & Guardrails */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div className="p-4 rounded-2xl bg-slate-950/40 border border-slate-800">
                        <span className="text-[11px] font-mono font-bold text-slate-300 uppercase block mb-2 flex items-center gap-1.5">
                          <Target className="w-3.5 h-3.5 text-indigo-400" /> Secondary Metrics:
                        </span>
                        <ul className="text-xs text-slate-400 space-y-1 list-disc list-inside">
                          {exp.secondary_metrics.map((sec, idx) => (
                            <li key={idx}><span className="text-slate-300">{sec}</span></li>
                          ))}
                        </ul>
                      </div>

                      <div className="p-4 rounded-2xl bg-slate-950/40 border border-slate-800">
                        <span className="text-[11px] font-mono font-bold text-slate-300 uppercase block mb-2 flex items-center gap-1.5">
                          <Shield className="w-3.5 h-3.5 text-rose-400" /> Guardrail Metrics:
                        </span>
                        <ul className="text-xs text-slate-400 space-y-1 list-disc list-inside">
                          {exp.guardrails.map((grd, idx) => (
                            <li key={idx}><span className="text-slate-300">{grd}</span></li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    {/* Decision Rule Card */}
                    <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 text-xs space-y-1.5">
                      <span className="font-mono font-bold text-amber-400 uppercase text-[11px] block">
                        Launch Decision Rule:
                      </span>
                      <p className="text-slate-300 leading-relaxed font-mono">{exp.decision_rule}</p>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
