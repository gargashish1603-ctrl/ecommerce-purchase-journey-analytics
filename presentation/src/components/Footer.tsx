"use client";

import React from "react";
import { Layers, ArrowUp, Sparkles } from "lucide-react";
import caseStudyData from "@/data/case-study-data.json";

export default function Footer() {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <footer className="bg-slate-950 border-t border-slate-800/80 py-12 text-slate-400 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-md bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-white">
                <Layers className="w-3.5 h-3.5" />
              </div>
              <span className="font-bold text-sm text-white tracking-tight">ShopSphere Analytics</span>
            </div>
            <p className="text-slate-400 max-w-md">
              E-commerce Purchase Journey Analytics & Conversion Optimization Case Study. Built for Product Analyst, Business Analyst, and Data Analyst portfolio presentations.
            </p>
          </div>

          <div className="flex items-center gap-4">
            <button
              onClick={scrollToTop}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 transition-colors border border-slate-800 font-mono text-[11px]"
            >
              <ArrowUp className="w-3.5 h-3.5" /> Back to Top
            </button>
          </div>
        </div>

        <div className="pt-6 border-t border-slate-800/60 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] font-mono text-slate-400">
          <div>
            Synthetic Dataset • 120,000 Sessions • Audited Observational Findings
          </div>
          <div>
            Built with Next.js 15, TypeScript & Tailwind CSS
          </div>
        </div>
      </div>
    </footer>
  );
}
