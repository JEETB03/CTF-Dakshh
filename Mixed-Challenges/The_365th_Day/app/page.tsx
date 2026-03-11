"use client";

import { useState, useEffect } from "react";
import StreakCard from "./components/streak-card";
import VaultQuestion from "./components/vault-question";

export default function Home() {
  const [vaultUnlocked, setVaultUnlocked] = useState(false);
  const [showVault, setShowVault] = useState(false);

  useEffect(() => {
    console.log(
      "%cTime travelers edit history. Maybe your browser remembers more than you think...",
      "color: #39ff14; font-size: 14px; font-family: monospace; text-shadow: 0 0 10px #39ff14;"
    );
  }, []);

  useEffect(() => {
    if (vaultUnlocked) {
      // Small delay for entrance animation
      const timer = setTimeout(() => setShowVault(true), 100);
      return () => clearTimeout(timer);
    }
  }, [vaultUnlocked]);

  return (
    <main className="ctf-main">
      {/* Scanline overlay */}
      <div className="scanline-overlay" />

      {/* Floating particles — deterministic values to avoid hydration mismatch */}
      <div className="particles">
        {[
          { l: 12, d: 0.2, t: 3.5 }, { l: 27, d: 1.1, t: 5.2 }, { l: 5, d: 2.3, t: 4.1 },
          { l: 42, d: 0.8, t: 6.3 }, { l: 68, d: 3.5, t: 3.9 }, { l: 85, d: 1.7, t: 5.7 },
          { l: 33, d: 4.2, t: 4.4 }, { l: 91, d: 0.5, t: 3.2 }, { l: 15, d: 2.9, t: 6.1 },
          { l: 58, d: 3.8, t: 4.8 }, { l: 76, d: 1.3, t: 5.5 }, { l: 49, d: 4.6, t: 3.7 },
          { l: 8, d: 0.9, t: 6.8 }, { l: 63, d: 2.1, t: 4.3 }, { l: 37, d: 3.3, t: 5.9 },
          { l: 94, d: 1.5, t: 3.4 }, { l: 22, d: 4.0, t: 6.5 }, { l: 71, d: 0.3, t: 4.6 },
          { l: 54, d: 2.7, t: 5.1 }, { l: 80, d: 3.1, t: 3.8 },
        ].map((p, i) => (
          <div
            key={i}
            className="particle"
            style={{
              left: `${p.l}%`,
              animationDelay: `${p.d}s`,
              animationDuration: `${p.t}s`,
            }}
          />
        ))}
      </div>

      {/* Grid background */}
      <div className="grid-bg" />

      <div className="ctf-container">
        {/* Header */}
        <header className="ctf-header">
          <div className="header-badge">CTF CHALLENGE</div>
          <div className="header-badge points-badge">POINTS — 150</div>
          <h1 className="ctf-title">
            <span className="title-icon">⏳</span>
            The 365th Day
          </h1>
          <p className="ctf-subtitle">
            Manipulate time if you dare.
          </p>
          <p className="flag-format">
            Flag Format: <code>dakshh&#123;...&#125;</code>
          </p>
          <div className="header-line" />
        </header>

        {/* Stage 1: Streak Card */}
        <section className="stage-section">
          <StreakCard onVaultUnlocked={() => setVaultUnlocked(true)} />
        </section>

        {/* Stage 2: Vault Question */}
        {vaultUnlocked && (
          <section className={`stage-section vault-section ${showVault ? "vault-visible" : ""}`}>
            <div className="stage-divider">
              <span className="stage-divider-text">⚡ STAGE 2 UNLOCKED ⚡</span>
            </div>
            <VaultQuestion />
          </section>
        )}

        {/* Footer */}
        <footer className="ctf-footer">
          <p>The 365th Day — CTF Challenge</p>
          <p className="footer-sub">What secrets does your browser hold?</p>
        </footer>
      </div>
    </main>
  );
}
