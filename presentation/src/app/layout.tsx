import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "ShopSphere | E-commerce Purchase Journey Analytics & Conversion Optimization",
  description:
    "A comprehensive product analytics case study investigating e-commerce purchase abandonment through event-level journey analysis, root-cause diagnosis, product requirements, and experimentation.",
  keywords: [
    "Product Analytics",
    "Customer Journey",
    "Funnel Analysis",
    "Conversion Optimization",
    "A/B Testing",
    "E-commerce",
    "Data Analysis",
  ],
  authors: [{ name: "Product & Data Analyst Portfolio" }],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable} scroll-smooth antialiased dark`}>
      <body className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
        {children}
      </body>
    </html>
  );
}
