import type { Metadata } from "next";
import { Geist_Mono } from "next/font/google";
import "./globals.css";

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "RaidCoach XIV — Mechanic Trainer",
  description:
    "Interactive FFXIV raid mechanic drills for M1S-M4S, M9S-M12S, and FRU. Train your positioning before prog night.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${geistMono.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col">
        <div className="fixed-bg" aria-hidden="true">
          <div className="aether-orb aether-orb-1" />
          <div className="aether-orb aether-orb-2" />
          <div className="aether-orb aether-orb-3" />
        </div>
        {children}
      </body>
    </html>
  );
}
