"use client";

import React from "react";
import { Terminal, Database, Code, Cpu, FileCode2, BookOpen, Layers } from "lucide-react";
import caseStudyData from "@/data/case-study-data.json";

export default function TechnicalDeepDiveSection() {
  const { tech_stack, repo_artifacts } = caseStudyData;

  return (
    <section id="tech" className="py-20 border-b border-slate-800/60 bg-slate-950/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="mb-10">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-2">
            <Terminal className="w-4 h-4" />
            Engineering & Analysis Architecture
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-white mb-2">
            Behind the Analysis
          </h2>
          <p className="text-sm text-slate-400 max-w-2xl">
            Raw clickstream event data was generated via a stochastic state-machine engine, validated across 17 integrity rules, transformed into analytical tables, and queried via DuckDB SQL and Python.
          </p>
        </div>

        {/* Tech Stack Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
          {/* Stack Categorization */}
          <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-6 space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider font-mono flex items-center gap-2">
              <Cpu className="w-4 h-4 text-indigo-400" /> Analytical & Engineering Stack
            </h3>
            <div className="space-y-3">
              {tech_stack.map((item, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs">
                  <div className="text-[11px] font-mono text-indigo-400 font-bold mb-0.5">{item.category}</div>
                  <div className="text-slate-200 font-mono">{item.tools}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Repository Artifacts */}
          <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-6 space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider font-mono flex items-center gap-2">
              <FileCode2 className="w-4 h-4 text-emerald-400" /> Repository Artifacts & Specs
            </h3>
            <div className="space-y-2.5">
              {repo_artifacts.map((art, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs flex items-center justify-between"
                >
                  <div>
                    <div className="font-semibold text-white mb-0.5">{art.title}</div>
                    <div className="font-mono text-[11px] text-slate-400">{art.path}</div>
                  </div>
                  <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                    {art.type}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Reproducibility Callout */}
        <div className="p-4 rounded-2xl bg-indigo-950/20 border border-indigo-800/40 flex items-center justify-between text-xs font-mono text-slate-400">
          <span>Random Seed: <strong className="text-indigo-300">SEED = 42</strong> (Deterministic Reproducibility)</span>
          <span className="text-slate-300">Engine: scripts/generate_data.py & scripts/run_analysis.py</span>
        </div>
      </div>
    </section>
  );
}
