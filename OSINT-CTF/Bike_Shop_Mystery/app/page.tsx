"use client";

import { useState, useEffect } from "react";

function Particles() {
  const [particles, setParticles] = useState<
    { id: number; x: number; color: string; size: number; duration: number; delay: number }[]
  >([]);

  useEffect(() => {
    const items = Array.from({ length: 30 }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      color: Math.random() > 0.5 ? "rgba(0, 240, 255, 0.4)" : "rgba(168, 85, 247, 0.3)",
      size: Math.random() * 2 + 1,
      duration: Math.random() * 15 + 10,
      delay: Math.random() * 10,
    }));
    setParticles(items);
  }, []);

  return (
    <div className="particles">
      {particles.map((p) => (
        <div
          key={p.id}
          className="particle"
          style={{
            left: `${p.x}%`,
            width: `${p.size}px`,
            height: `${p.size}px`,
            backgroundColor: p.color,
            animationDuration: `${p.duration}s`,
            animationDelay: `${p.delay}s`,
          }}
        />
      ))}
    </div>
  );
}

export default function Home() {
  const [lightbox, setLightbox] = useState(false);

  const hasImage = true;

  return (
    <>
      <Particles />

      {lightbox && hasImage && (
        <div className="lightbox" onClick={() => setLightbox(false)}>
          <button className="lightbox-close" onClick={() => setLightbox(false)}>
            ✕
          </button>
          <img src="/challenge.jpg" alt="Kyoto Bike Shop" />
        </div>
      )}

      <main className="challenge-container">
        {/* Header */}
        <header className="challenge-header">
          <div className="header-badge">
            <span className="dot" />
            OSINT Challenge Active
          </div>
          <h1 className="challenge-title">Kyoto Bike Shop Mystery</h1>
          <p className="challenge-subtitle">
            Use your Open Source Intelligence skills to identify this bike shop in Kyoto and find its phone number.
          </p>
        </header>

        {/* Challenge Card */}
        <div className="challenge-card">
          <div className="card-header">
            <div className="card-header-left">
              <div className="card-icon">🚲</div>
              <div>
                <div className="card-label">Challenge</div>
                <div className="card-name">Find the Phone Number</div>
              </div>
            </div>
            <div className="difficulty-badge difficulty-medium">300 Points</div>
          </div>

          <div className="card-body">
            {/* Mission */}
            <div className="mission-section">
              <div className="mission-label">
                <span>📋</span> Mission Briefing
              </div>
              <p className="mission-text">
                The bikes I saw in this shop in Kyoto look beautiful! I&apos;d love to know where to buy one.{" "}
                <strong>Find the phone number of this store</strong> and submit it as the flag in the format:{" "}
                <code
                  style={{
                    background: "rgba(0, 240, 255, 0.08)",
                    padding: "0.15rem 0.5rem",
                    borderRadius: "4px",
                    fontFamily: "'JetBrains Mono', monospace",
                    fontSize: "0.8rem",
                    color: "var(--accent-cyan)",
                  }}
                >
                  dakshh&#123;phone_number&#125;
                </code>
              </p>
            </div>

            {/* Image */}
            <div className="image-section">
              <div className="mission-label">
                <span>🖼️</span> Evidence
              </div>
              <div
                className="image-wrapper"
                onClick={() => hasImage && setLightbox(true)}
              >
                {hasImage ? (
                  <>
                    <img src="/challenge.jpg" alt="A bike shop in Kyoto, Japan" />
                    <div className="image-overlay">
                      <span className="image-hint">Click to enlarge</span>
                      <button className="zoom-btn" onClick={(e) => { e.stopPropagation(); setLightbox(true); }}>
                        🔍
                      </button>
                    </div>
                  </>
                ) : (
                  <div className="image-placeholder">
                    <div className="image-placeholder-icon">📷</div>
                    <div className="image-placeholder-text">Image will be placed here</div>
                    <div style={{ fontSize: "0.65rem", color: "var(--text-muted)", fontFamily: "'JetBrains Mono', monospace" }}>
                      Add challenge.jpg to /public folder
                    </div>
                  </div>
                )}
              </div>
            </div>


          </div>

        </div>

        {/* Footer */}
        <footer className="challenge-footer">
          OSINTC-TF &bull; Open Source Intelligence Challenge &bull; 2026
        </footer>
      </main>
    </>
  );
}
