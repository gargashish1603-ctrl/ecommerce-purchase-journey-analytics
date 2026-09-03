"use client";

import React from "react";
import Navbar from "@/components/Navbar";
import HeroSection from "@/components/HeroSection";
import JourneyExplorerSection from "@/components/JourneyExplorerSection";
import FunnelDiagnosisSection from "@/components/FunnelDiagnosisSection";
import RootCausePrioritySection from "@/components/RootCausePrioritySection";
import EvidenceBoardSection from "@/components/EvidenceBoardSection";
import HypothesisScorecardSection from "@/components/HypothesisScorecardSection";
import ProductTranslationSection from "@/components/ProductTranslationSection";
import ExperimentPortfolioSection from "@/components/ExperimentPortfolioSection";
import DecisionFrameworkSection from "@/components/DecisionFrameworkSection";
import TraceabilityMatrixSection from "@/components/TraceabilityMatrixSection";
import ResearchGapsSection from "@/components/ResearchGapsSection";
import TechnicalDeepDiveSection from "@/components/TechnicalDeepDiveSection";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Fixed Navigation */}
      <Navbar />

      {/* Main Content Sections */}
      <main className="flex-1 space-y-0">
        {/* Section 1: Hero & Executive Summary */}
        <HeroSection />

        {/* Section 2: Interactive Customer Journey */}
        <JourneyExplorerSection />

        {/* Section 3: Funnel Diagnosis & Drop-off Breakdown */}
        <FunnelDiagnosisSection />

        {/* Section 4: Root-Cause Prioritization Matrix */}
        <RootCausePrioritySection />

        {/* Section 5: Key Evidence Board */}
        <EvidenceBoardSection />

        {/* Section 6: Hypothesis Scorecard (H1–H10) */}
        <HypothesisScorecardSection />

        {/* Section 7: Insight-to-Product Translation */}
        <ProductTranslationSection />

        {/* Section 8: Experimentation Portfolio (EXP-01 to EXP-04) */}
        <ExperimentPortfolioSection />

        {/* Section 9: Experiment Launch Decision Framework */}
        <DecisionFrameworkSection />

        {/* Section 10: Requirements Traceability Matrix */}
        <TraceabilityMatrixSection />

        {/* Section 11: Limitations & Qualitative Research Gaps */}
        <ResearchGapsSection />

        {/* Section 12: Behind the Analysis (Technical Deep Dive) */}
        <TechnicalDeepDiveSection />
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}
