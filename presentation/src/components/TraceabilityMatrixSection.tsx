"use client";

import React, { useState } from "react";
import { Link2, ExternalLink, ChevronDown, ChevronUp, FileCode } from "lucide-react";
import caseStudyData from "@/data/case-study-data.json";

export default function TraceabilityMatrixSection() {
  const { traceability_sample } = caseStudyData;
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  return (
    <section id="traceability" className="py-20 border-b border-slate-800/60 bg-slate-950/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="mb-10">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-2">
            <Link2 className="w-4 h-4" />
            End-to-End Governance
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-white mb-2">
            Requirements Traceability Matrix (RTM)
          </h2>
          <p className="text-sm text-slate-400 max-w-2xl">
            Verifying zero orphan requirements and zero speculative experiments. Every engineering requirement traces backwards to empirical clickstream evidence and forward to candidate A/B testing KPIs.
          </p>
        </div>

        {/* Lightweight Traceability Table */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-3xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-950 text-slate-400 font-mono text-[11px] uppercase border-b border-slate-800">
                <tr>
                  <th className="px-5 py-3.5">Problem ID</th>
                  <th className="px-5 py-3.5">Empirical Evidence Base</th>
                  <th className="px-5 py-3.5">Business Req</th>
                  <th className="px-5 py-3.5">Candidate Experiment</th>
                  <th className="px-5 py-3.5 text-emerald-400">Primary Success KPI</th>
                  <th className="px-5 py-3.5 text-right">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-200">
                {traceability_sample.map((row, idx) => {
                  const isExpanded = expandedIndex === idx;

                  return (
                    <React.Fragment key={idx}>
                      <tr className="hover:bg-slate-850/50 transition-colors">
                        <td className="px-5 py-4 font-mono font-bold text-indigo-400">{row.problem_id}</td>
                        <td className="px-5 py-4 font-mono text-slate-300 max-w-xs truncate">{row.evidence}</td>
                        <td className="px-5 py-4 font-mono text-slate-400">{row.business_req.split(" ")[0]}</td>
                        <td className="px-5 py-4 font-bold text-white">{row.experiment}</td>
                        <td className="px-5 py-4 font-mono text-emerald-400">{row.primary_kpi}</td>
                        <td className="px-5 py-4 text-right">
                          <button
                            onClick={() => setExpandedIndex(isExpanded ? null : idx)}
                            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
                            aria-label="Toggle row details"
                          >
                            {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                          </button>
                        </td>
                      </tr>

                      {isExpanded && (
                        <tr className="bg-slate-950/80">
                          <td colSpan={6} className="px-6 py-5 border-b border-slate-800/80">
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-mono">
                              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                                <span className="text-[10px] text-slate-400 uppercase block mb-1">Functional Specs:</span>
                                <span className="text-slate-200">{row.functional_req}</span>
                              </div>
                              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                                <span className="text-[10px] text-slate-400 uppercase block mb-1">Non-Functional Constraints:</span>
                                <span className="text-slate-200">{row.nfr}</span>
                              </div>
                              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                                <span className="text-[10px] text-slate-400 uppercase block mb-1">Acceptance Criteria:</span>
                                <span className="text-slate-200">{row.acceptance_criteria}</span>
                              </div>
                            </div>
                          </td>
                        </tr>
                      )}
                    </React.Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>

          <div className="p-4 bg-slate-950/60 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
            <span>Showing core high-priority traceability pathways</span>
            <span className="font-mono text-[11px] text-indigo-400">
              Full matrix: product/requirements-traceability-matrix.md
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
