"use client";

import React, { useState } from "react";
import { ChevronRight, ArrowDownRight, Compass, Users, Activity, FileText, CheckCircle2, AlertTriangle } from "lucide-react";
import caseStudyData from "@/data/case-study-data.json";

export default function JourneyExplorerSection() {
  const { journey_stages } = caseStudyData;
  const [selectedStageId, setSelectedStageId] = useState<number>(6); // Default to Address Entry (P0 focus)

  const selectedStage = journey_stages.find((s) => s.id === selectedStageId) || journey_stages[5];

  return (
    <section id="journey" className="py-20 border-b border-slate-800/60 bg-slate-950/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="mb-10">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-2">
            <Compass className="w-4 h-4" />
            Interactive Journey Architecture
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-white mb-2">
            The Customer Purchase Journey
          </h2>
          <p className="text-sm text-slate-400 max-w-2xl">
            Click across any of the 11 sequential clickstream touchpoints to inspect stage-specific session volume, dropout friction, behavioral characteristics, and empirical findings.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left Column: Interactive Stage Selector Strip */}
          <div className="lg:col-span-7 space-y-2">
            <div className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-3 px-1 flex items-center justify-between">
              <span>Sequential Journey Stages</span>
              <span className="text-[11px] text-indigo-400">Click to Inspect Stage</span>
            </div>

            <div className="space-y-1.5">
              {journey_stages.map((stage) => {
                const isSelected = stage.id === selectedStageId;
                const isMajorLeak = stage.id === 2 || stage.id === 4 || stage.id === 6 || stage.id === 7 || stage.id === 9;

                return (
                  <button
                    key={stage.id}
                    onClick={() => setSelectedStageId(stage.id)}
                    className={`w-full text-left px-4 py-3 rounded-xl border transition-all flex items-center justify-between ${
                      isSelected
                        ? "bg-indigo-950/60 border-indigo-500/60 shadow-md shadow-indigo-950/40 text-white"
                        : "bg-slate-900/30 border-slate-800/70 hover:bg-slate-900/60 hover:border-slate-700 text-slate-300"
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span
                        className={`w-6 h-6 rounded-md flex items-center justify-center text-xs font-mono font-semibold ${
                          isSelected
                            ? "bg-indigo-500 text-white"
                            : "bg-slate-800 text-slate-400"
                        }`}
                      >
                        {stage.id}
                      </span>
                      <div>
                        <div className="text-xs font-semibold text-white flex items-center gap-2">
                          {stage.name}
                          {isMajorLeak && (
                            <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-amber-950/50 text-amber-300 border border-amber-800/40">
                              Drop-off Gate
                            </span>
                          )}
                        </div>
                        <div className="text-[11px] font-mono text-slate-400">
                          event: <span className="text-indigo-300">{stage.event}</span>
                        </div>
                      </div>
                    </div>

                    <div className="text-right">
                      <div className="text-xs font-mono font-bold text-slate-200">
                        {stage.sessions_reached.toLocaleString()} <span className="text-[10px] font-normal text-slate-400">sess</span>
                      </div>
                      <div className="text-[10px] font-mono text-slate-400">
                        {stage.traffic_share} reach
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Right Column: Dynamic Stage Inspector Card */}
          <div className="lg:col-span-5 sticky top-24">
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
              <div className="absolute top-0 right-0 w-48 h-48 bg-indigo-500/10 rounded-full blur-2xl pointer-events-none" />

              {/* Inspector Header */}
              <div className="flex items-center justify-between pb-4 mb-5 border-b border-slate-800">
                <div>
                  <div className="text-[11px] font-mono uppercase text-indigo-400 font-semibold tracking-wider">
                    Stage {selectedStage.id} of 11
                  </div>
                  <h3 className="text-xl font-bold text-white">{selectedStage.name}</h3>
                </div>
                <div className="px-2.5 py-1 rounded-lg bg-slate-800/80 border border-slate-700 text-xs font-mono text-slate-300">
                  {selectedStage.event}
                </div>
              </div>

              {/* Stage Metrics Grid */}
              <div className="grid grid-cols-2 gap-3 mb-5">
                <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
                  <div className="text-[11px] text-slate-400">Sessions Reached</div>
                  <div className="text-lg font-mono font-bold text-white">
                    {selectedStage.sessions_reached.toLocaleString()}
                  </div>
                  <div className="text-[10px] text-slate-400">{selectedStage.traffic_share} of total traffic</div>
                </div>

                <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
                  <div className="text-[11px] text-slate-400">Pass / Drop Status</div>
                  <div className="text-lg font-mono font-bold text-indigo-300">
                    {selectedStage.pass_rate}
                  </div>
                  <div className="text-[10px] text-slate-400">
                    {selectedStage.dropoff_sessions > 0
                      ? `${selectedStage.dropoff_sessions.toLocaleString()} drops at this step`
                      : "Zero drop gate"}
                  </div>
                </div>
              </div>

              {/* Description */}
              <div className="space-y-4 text-xs text-slate-300 mb-6">
                <div>
                  <span className="font-semibold text-slate-200 block mb-1">What the customer is doing:</span>
                  <p className="text-slate-400 leading-relaxed">{selectedStage.description}</p>
                </div>

                <div className="p-3.5 rounded-xl bg-indigo-950/30 border border-indigo-800/40">
                  <span className="font-semibold text-indigo-300 flex items-center gap-1.5 mb-1 text-xs">
                    <Activity className="w-3.5 h-3.5 text-indigo-400" />
                    Key Analytical Finding:
                  </span>
                  <p className="text-slate-300 leading-relaxed text-xs">{selectedStage.key_finding}</p>
                </div>
              </div>

              {/* Source Document Reference */}
              <div className="pt-4 border-t border-slate-800 flex items-center justify-between text-[11px] font-mono text-slate-400">
                <span>Repository Source:</span>
                <span className="text-indigo-400 bg-slate-800/50 px-2 py-0.5 rounded border border-slate-700/60">
                  {selectedStage.doc_ref}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
