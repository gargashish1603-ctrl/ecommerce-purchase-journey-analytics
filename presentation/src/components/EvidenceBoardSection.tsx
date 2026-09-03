"use client";

import React, { useState } from "react";
import { BarChart2, Smartphone, Truck, CreditCard, Tag, Search, CheckCircle2, TrendingDown } from "lucide-react";
import caseStudyData from "@/data/case-study-data.json";

export default function EvidenceBoardSection() {
  const { evidence_board } = caseStudyData;
  const [activeTab, setActiveTab] = useState<"address" | "shipping" | "payment" | "promo" | "browsing">("address");

  const tabs = [
    { key: "address", label: "Mobile Address", icon: Smartphone },
    { key: "shipping", label: "Shipping Fee Elasticity", icon: Truck },
    { key: "payment", label: "Payment Gateway", icon: CreditCard },
    { key: "promo", label: "Promo Validation", icon: Tag },
    { key: "browsing", label: "Browsing Depth", icon: Search },
  ];

  return (
    <section id="evidence" className="py-20 border-b border-slate-800/60 bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="mb-10">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-2">
            <BarChart2 className="w-4 h-4" />
            Statistical Findings & Evidence
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-white mb-2">
            The Analytical Evidence Board
          </h2>
          <p className="text-sm text-slate-400 max-w-2xl">
            Inspect the regression coefficients, non-parametric test statistics, and cohort breakdowns supporting each diagnostic finding.
          </p>
        </div>

        {/* Tab Selector */}
        <div className="flex flex-wrap gap-2 mb-8 p-1.5 bg-slate-900/80 border border-slate-800 rounded-2xl">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.key;
            return (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key as any)}
                className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-medium transition-all ${
                  isActive
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                    : "text-slate-400 hover:text-white hover:bg-slate-800/50"
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Dynamic Evidence Content */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-6 sm:p-8">
          {/* TAB 1: Mobile Address */}
          {activeTab === "address" && (
            <div className="space-y-6">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
                <div>
                  <h3 className="text-xl font-bold text-white mb-1">{evidence_board.mobile_address.title}</h3>
                  <p className="text-xs text-slate-400">Multivariate logistic regression controlling for acquisition channel and customer maturity</p>
                </div>
                <div className="text-right">
                  <span className="text-xs font-mono font-bold text-rose-400 px-3 py-1 rounded-full bg-rose-950/60 border border-rose-800/60">
                    {evidence_board.mobile_address.gap}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Mobile Pass Rate</div>
                  <div className="text-xl font-mono font-bold text-white">{evidence_board.mobile_address.primary_metric}</div>
                  <div className="text-[10px] text-slate-400">10,483 / 13,239 mobile starters</div>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Desktop Pass Rate</div>
                  <div className="text-xl font-mono font-bold text-emerald-400">{evidence_board.mobile_address.comparison_metric}</div>
                  <div className="text-[10px] text-slate-400">5,217 / 5,992 desktop starters</div>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Adjusted Odds Ratio</div>
                  <div className="text-xl font-mono font-bold text-indigo-300">OR = {evidence_board.mobile_address.adj_or}</div>
                  <div className="text-[10px] text-slate-400">95% CI: {evidence_board.mobile_address.ci_95} (p = 4.48e-37)</div>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Excess Lost Sessions</div>
                  <div className="text-xl font-mono font-bold text-rose-300">{evidence_board.mobile_address.excess_loss}</div>
                  <div className="text-[10px] text-slate-400">Attributable above desktop rate</div>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-indigo-950/30 border border-indigo-800/40 text-xs text-slate-300 leading-relaxed">
                <span className="font-semibold text-indigo-300 block mb-1">Analytical Interpretation:</span>
                {evidence_board.mobile_address.interpretation}
              </div>
            </div>
          )}

          {/* TAB 2: Shipping */}
          {activeTab === "shipping" && (
            <div className="space-y-6">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
                <div>
                  <h3 className="text-xl font-bold text-white mb-1">{evidence_board.shipping.title}</h3>
                  <p className="text-xs text-slate-400">Evaluation of fee-to-cart ratio and $75 free shipping threshold discontinuity</p>
                </div>
                <span className="text-xs font-mono font-bold text-amber-400 px-3 py-1 rounded-full bg-amber-950/60 border border-amber-800/60">
                  24.20% Sub-$75 Drop-off Rate
                </span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Sub-$75 Shipping Drops</div>
                  <div className="text-xl font-mono font-bold text-white">{evidence_board.shipping.sub75_shipping_dropouts.toLocaleString()}</div>
                  <div className="text-[10px] text-slate-400">73.1% of all shipping dropouts</div>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Total Shipping Drops</div>
                  <div className="text-xl font-mono font-bold text-slate-200">{evidence_board.shipping.total_shipping_dropouts.toLocaleString()}</div>
                  <div className="text-[10px] text-slate-400">Across all basket sizes</div>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Fee Ratio Elasticity</div>
                  <div className="text-xl font-mono font-bold text-indigo-300">OR_10% = 1.493</div>
                  <div className="text-[10px] text-slate-400">Per +10pp ratio increase (p &lt; 10^-100)</div>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Near-Threshold Backtrack</div>
                  <div className="text-xl font-mono font-bold text-amber-300">{evidence_board.shipping.backtracking_rate}</div>
                  <div className="text-[10px] text-slate-400">In $60-$74.99 basket band</div>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-indigo-950/30 border border-indigo-800/40 text-xs text-slate-300 leading-relaxed">
                <span className="font-semibold text-indigo-300 block mb-1">Analytical Interpretation:</span>
                {evidence_board.shipping.interpretation}
              </div>
            </div>
          )}

          {/* TAB 3: Payment */}
          {activeTab === "payment" && (
            <div className="space-y-6">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
                <div>
                  <h3 className="text-xl font-bold text-white mb-1">{evidence_board.payment.title}</h3>
                  <p className="text-xs text-slate-400">State-transition audit of payment failure attempts, retry pathways, and net recovery</p>
                </div>
                <span className="text-xs font-mono font-bold text-rose-400 px-3 py-1 rounded-full bg-rose-950/60 border border-rose-800/60">
                  409 Permanent Lost Orders
                </span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Failed Payment Sessions</div>
                  <div className="text-xl font-mono font-bold text-white">{evidence_board.payment.failed_sessions}</div>
                  <div className="text-[10px] text-slate-400">{evidence_board.payment.decline_rate}</div>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Organic Recovery Rate</div>
                  <div className="text-xl font-mono font-bold text-emerald-400">{evidence_board.payment.recovery_rate}</div>
                  <div className="text-[10px] text-slate-400">448 sessions recovered</div>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Immediate Exit Rate</div>
                  <div className="text-xl font-mono font-bold text-rose-300">{evidence_board.payment.immediate_exit_rate}</div>
                  <div className="text-[10px] text-slate-400">Exit within 30s with 0 retries</div>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Instrument Performance</div>
                  <div className="text-xs font-mono font-semibold text-indigo-300">Wallets: 3.4%</div>
                  <div className="text-[10px] text-slate-400">vs Net Banking 11.6%</div>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-indigo-950/30 border border-indigo-800/40 text-xs text-slate-300 leading-relaxed">
                <span className="font-semibold text-indigo-300 block mb-1">Analytical Interpretation:</span>
                {evidence_board.payment.interpretation}
              </div>
            </div>
          )}

          {/* TAB 4: Promo */}
          {activeTab === "promo" && (
            <div className="space-y-6">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
                <div>
                  <h3 className="text-xl font-bold text-white mb-1">{evidence_board.promo.title}</h3>
                  <p className="text-xs text-slate-400">Cart progression and conversion impact of promo code validation rejections</p>
                </div>
                <span className="text-xs font-mono font-bold text-rose-400 px-3 py-1 rounded-full bg-rose-950/60 border border-rose-800/60">
                  {evidence_board.promo.progression_deficit}
                </span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Invalid Promo Sessions</div>
                  <div className="text-xl font-mono font-bold text-white">{evidence_board.promo.invalid_promo_sessions.toLocaleString()}</div>
                  <div className="text-[10px] text-slate-400">Encountered ERR_INVALID_PROMO</div>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Invalid Cart Checkout Rate</div>
                  <div className="text-xl font-mono font-bold text-rose-400">{evidence_board.promo.checkout_rate_invalid}</div>
                  <div className="text-[10px] text-slate-400">vs 62.57% for non-promo carts</div>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Lost Cart Sessions</div>
                  <div className="text-xl font-mono font-bold text-amber-300">{evidence_board.promo.lost_cart_sessions}</div>
                  <div className="text-[10px] text-slate-400">Pre-checkout cart abandonments</div>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[11px] text-slate-400 mb-1">Session CVR Impact</div>
                  <div className="text-xl font-mono font-bold text-slate-200">26.56%</div>
                  <div className="text-[10px] text-slate-400">vs 40.32% for non-promo</div>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-indigo-950/30 border border-indigo-800/40 text-xs text-slate-300 leading-relaxed">
                <span className="font-semibold text-indigo-300 block mb-1">Analytical Interpretation:</span>
                {evidence_board.promo.interpretation}
              </div>
            </div>
          )}

          {/* TAB 5: Browsing Depth */}
          {activeTab === "browsing" && (
            <div className="space-y-6">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
                <div>
                  <h3 className="text-xl font-bold text-white mb-1">{evidence_board.browsing.title}</h3>
                  <p className="text-xs text-slate-400">Canonical browsing depth progression series and correlation analysis</p>
                </div>
                <span className="text-xs font-mono font-bold text-indigo-300 px-3 py-1 rounded-full bg-indigo-950/60 border border-indigo-800/60">
                  {evidence_board.browsing.correlation}
                </span>
              </div>

              {/* Table of Canonical Browsing Series */}
              <div className="overflow-x-auto">
                <table className="w-full text-xs text-left">
                  <thead className="bg-slate-950 text-slate-400 font-mono text-[11px] uppercase border-b border-slate-800">
                    <tr>
                      <th className="px-4 py-3">Browsing Depth Tier</th>
                      <th className="px-4 py-3">Sessions</th>
                      <th className="px-4 py-3">Traffic Share</th>
                      <th className="px-4 py-3">Cart Add Rate</th>
                      <th className="px-4 py-3 text-indigo-300">Session CVR</th>
                      <th className="px-4 py-3 text-emerald-300">Cart-to-Purchase CVR</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800 font-mono text-slate-200">
                    {evidence_board.browsing.tiers.map((row, idx) => (
                      <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                        <td className="px-4 py-3 font-semibold text-white">{row.tier}</td>
                        <td className="px-4 py-3">{row.sessions.toLocaleString()}</td>
                        <td className="px-4 py-3">{row.traffic_share}</td>
                        <td className="px-4 py-3">{row.cart_add_rate}</td>
                        <td className="px-4 py-3 font-bold text-indigo-300">{row.session_cvr}</td>
                        <td className="px-4 py-3 font-bold text-emerald-400">{row.cart_to_purchase}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="p-4 rounded-xl bg-indigo-950/30 border border-indigo-800/40 text-xs text-slate-300 leading-relaxed">
                <span className="font-semibold text-indigo-300 block mb-1">Canonical Analytical Takeaway:</span>
                {evidence_board.browsing.interpretation}
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
