"use client";

import React, { useState } from "react";
import { Filter, ArrowDown, TrendingDown, Layers, ShieldAlert, Sparkles, PieChart } from "lucide-react";
import caseStudyData from "@/data/case-study-data.json";

export default function FunnelDiagnosisSection() {
  const { funnel_summary } = caseStudyData;
  const [activeTab, setActiveTab] = useState<"macro" | "leakage">("macro");

  const funnelBars = [
    { label: "Marketplace Sessions", count: 120000, pct: 100, color: "bg-indigo-500", subtext: "Total inbound traffic (100.0%)" },
    { label: "Cart Additions", count: 32354, pct: 26.96, color: "bg-violet-500", subtext: "26.96% of total site traffic" },
    { label: "Checkout Starters", count: 19931, pct: 16.61, color: "bg-purple-500", subtext: "61.60% of cart add sessions" },
    { label: "Completed Orders", count: 12888, pct: 10.74, color: "bg-emerald-500", subtext: "64.66% of checkout starters (10.74% overall CVR)" },
  ];

  const lossBreakdown = [
    {
      category: "Discovery-Stage Bouncers",
      sessions: 87646,
      share: "81.83%",
      intent: "Low (Casual / Bouncers)",
      dwell: "49s median",
      description: "Visitors exploring 1-3 products who exit without adding any item to cart.",
      color: "border-slate-700 bg-slate-900/40 text-slate-300",
    },
    {
      category: "Pre-Checkout Cart Abandoners",
      sessions: 12423,
      share: "11.60%",
      intent: "Medium-High (Cart Intent)",
      dwell: "63s median ($104 ACV)",
      description: "Shoppers who built a basket but exited before starting checkout (impacted by promo code friction).",
      color: "border-amber-800/60 bg-amber-950/20 text-amber-300",
    },
    {
      category: "Active Checkout Leaks",
      sessions: 7043,
      share: "6.57%",
      intent: "Highest (Committed Buyers)",
      dwell: "127s - 167s median",
      description: "Shoppers who initiated checkout and dropped out across Address (3,621), Shipping (2,143), and Payment (1,279).",
      color: "border-rose-800/60 bg-rose-950/20 text-rose-300",
    },
  ];

  return (
    <section id="funnel" className="py-20 border-b border-slate-800/60 bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-2">
              <Filter className="w-4 h-4" />
              Funnel Conversion Decomposition
            </div>
            <h2 className="text-3xl font-bold tracking-tight text-white mb-2">
              Macro Funnel & Journey Drop-off Breakdown
            </h2>
            <p className="text-sm text-slate-400 max-w-2xl">
              Distinguishing top-of-funnel discovery loss from high-severity checkout drop-off.
            </p>
          </div>

          {/* Tab Selector */}
          <div className="flex items-center bg-slate-900 border border-slate-800 p-1 rounded-xl">
            <button
              onClick={() => setActiveTab("macro")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                activeTab === "macro"
                  ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              Macro Funnel View
            </button>
            <button
              onClick={() => setActiveTab("leakage")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                activeTab === "leakage"
                  ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              Loss Category Matrix
            </button>
          </div>
        </div>

        {/* Headline Insight Banner */}
        <div className="p-4 rounded-xl bg-indigo-950/40 border border-indigo-800/50 mb-8 flex items-start gap-3">
          <Sparkles className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />
          <div className="text-xs text-slate-300 leading-relaxed">
            <span className="font-semibold text-white">Headline Funnel Insight: </span>
            {funnel_summary.headline_insight}
          </div>
        </div>

        {activeTab === "macro" ? (
          /* Macro Funnel Visual */
          <div className="space-y-4 bg-slate-900/40 border border-slate-800 rounded-2xl p-6">
            <div className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2">
              Marketplace Progression Hierarchy
            </div>

            {funnelBars.map((bar, idx) => (
              <div key={idx} className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-white flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-slate-400" />
                    {bar.label}
                  </span>
                  <span className="font-mono text-slate-200">
                    {bar.count.toLocaleString()} <span className="text-slate-400">({bar.pct}%)</span>
                  </span>
                </div>

                {/* Progress bar container */}
                <div className="h-7 w-full bg-slate-950 rounded-lg overflow-hidden p-1 border border-slate-800 flex items-center">
                  <div
                    className={`h-full rounded-md ${bar.color} transition-all duration-700 relative`}
                    style={{ width: `${Math.max(bar.pct, 4)}%` }}
                  />
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-400 px-1 font-mono">
                  <span>{bar.subtext}</span>
                  {idx < funnelBars.length - 1 && (
                    <span className="text-rose-400 font-medium">
                      ↓ -{(funnelBars[idx].count - funnelBars[idx + 1].count).toLocaleString()} lost
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          /* Loss Category Decomposition Cards */
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {lossBreakdown.map((item, idx) => (
              <div key={idx} className={`p-5 rounded-2xl border ${item.color} flex flex-col justify-between`}>
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-[10px] font-mono uppercase font-bold px-2 py-0.5 rounded bg-slate-950/60 border border-slate-800">
                      Tier {idx + 1}
                    </span>
                    <span className="text-xs font-mono font-bold">{item.share} of losses</span>
                  </div>

                  <h3 className="text-base font-bold text-white mb-1">{item.category}</h3>
                  <div className="text-2xl font-mono font-bold text-white mb-2">
                    {item.sessions.toLocaleString()} <span className="text-xs font-normal text-slate-400">sessions</span>
                  </div>

                  <p className="text-xs text-slate-300 leading-relaxed mb-4">{item.description}</p>
                </div>

                <div className="pt-3 border-t border-slate-800/80 space-y-1 text-[11px] font-mono">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Intent Level:</span>
                    <span className="text-slate-200 font-medium">{item.intent}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Behavior Profile:</span>
                    <span className="text-slate-200 font-medium">{item.dwell}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
