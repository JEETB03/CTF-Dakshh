"use client";

import { useState, useRef, useCallback, useEffect } from "react";

type ConfettiPieceType = { id: number; left: string; color: string; delay: string; size: string; shape: string };



export default function HomePage() {
  const [fullscreen, setFullscreen] = useState<boolean>(false);
  const [zoomed, setZoomed] = useState<boolean>(false);
  const [rotation, setRotation] = useState<number>(0);
  const [zoomOrigin, setZoomOrigin] = useState<{ x: string; y: string }>({ x: "50%", y: "50%" });
  const [elapsedTime, setElapsedTime] = useState<number>(0);
  const [confetti, setConfetti] = useState<ConfettiPieceType[]>([]);

  const viewerRef = useRef<HTMLDivElement>(null);
  const imgRef = useRef<HTMLImageElement>(null);

  // Timer
  useEffect(() => {
    const timer = setInterval(() => {
      setElapsedTime((t) => t + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  const handleMouseMove = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      if (!viewerRef.current) return;
      const rect = viewerRef.current.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      setZoomOrigin({ x: x + "%", y: y + "%" });
    },
    []
  );

  // Floating particles
  const [particles, setParticles] = useState<{ id: number; left: string; size: string; duration: string; delay: string; opacity: number }[]>([]);

  useEffect(() => {
    setParticles(
      Array.from({ length: 20 }, (_, i) => ({
        id: i,
        left: Math.random() * 100 + "%",
        size: Math.random() * 3 + 1 + "px",
        duration: Math.random() * 15 + 10 + "s",
        delay: Math.random() * 10 + "s",
        opacity: Math.random() * 0.4 + 0.1,
      }))
    );
  }, []);

  return (
    <>
      {/* Floating particles */}
      <div className="particles">
        {particles.map((p) => (
          <div
            key={p.id}
            className="particle"
            style={{
              left: p.left,
              width: p.size,
              height: p.size,
              animationDuration: p.duration,
              animationDelay: p.delay,
            }}
          />
        ))}
      </div>

      <main className="main">
        {/* Hero Section */}
        <div className="hero-section">
          <div className="hero-badge">
            <span className="badge-dot"></span>
            ACTIVE INVESTIGATION
          </div>
          <h1 className="hero-title">Wheels of Truth</h1>
          <p className="hero-subtitle">
            Uncover the truth behind this holiday snapshot. Use OSINT techniques to identify the bus company, route number, and registration.
          </p>
        </div>




        {/* Content Grid */}
        <div className="content-grid">
          <div className="left-column">
            {/* Evidence Card */}
            <div className="card" style={{ marginBottom: "2rem" }}>
              <div className="card-header">
                <div className="card-header-title">
                  <span className="icon">📸</span> Holiday Photo
                </div>
              </div>
              <div className="card-body" style={{ padding: 0 }}>
                <div
                  className={`evidence-viewer${zoomed ? " zoomed" : ""}`}
                  ref={viewerRef}
                  onMouseMove={handleMouseMove}
                  onClick={() => setZoomed((z) => !z)}
                  style={{
                    // @ts-ignore
                    "--zoom-x": zoomOrigin.x,
                    "--zoom-y": zoomOrigin.y,
                  }}
                >
                  <div className="evidence-label">Evidence #1</div>
                  <img
                    ref={imgRef}
                    src="/buses.png"
                    alt="Holiday bus photo evidence"
                    style={{ transform: `${zoomed ? "scale(2.5)" : "scale(1)"} rotate(${rotation}deg)` }}
                    draggable={false}
                  />
                  <div className="evidence-toolbar">
                    <button
                      title="Full Screen"
                      onClick={(e) => {
                        e.stopPropagation();
                        setFullscreen(true);
                      }}
                    >
                      ⛶
                    </button>
                    <a
                      href="/buses.png"
                      download="holiday_bus_evidence.png"
                      title="Download"
                      onClick={(e) => e.stopPropagation()}
                      style={{ display: "inline-flex", alignItems: "center", justifyContent: "center" }}
                    >
                      <button onClick={(e) => e.stopPropagation()}>
                        ⬇️
                      </button>
                    </a>
                  </div>
                </div>
              </div>
            </div>

            {/* Challenge Briefing */}
            <div className="card" style={{ marginBottom: "2rem" }}>
              <div className="card-header">
                <div className="card-header-title">
                  <span className="icon">📋</span> Challenge Briefing
                </div>
              </div>
              <div className="card-body">
                <p className="challenge-text">
                  <em>
                    While on holiday I really enjoyed riding the furthest left bus in this image.
                    Some would call me obsessed, but I&apos;d love to know more about it.
                  </em>
                </p>
                <p className="challenge-text" style={{ marginTop: "1rem" }}>
                  Your mission is to investigate the image and identify key details about the bus.
                  Using OSINT techniques, determine:
                </p>
                <ul className="challenge-objectives">
                  <li>
                    <span className="obj-icon">1</span>
                    The bus company name
                  </li>
                  <li>
                    <span className="obj-icon">2</span>
                    The bus route / number
                  </li>
                  <li>
                    <span className="obj-icon">3</span>
                    The vehicle&apos;s registration number
                  </li>
                </ul>
                <div className="flag-format">
                  <strong>Flag Format:</strong>
                  <br />
                  <code>dakshh&#123;bus_company_name_bus_route_number_registration_number&#125;</code>
                  <br />
                  <br />
                  <strong>Rules:</strong>
                  <br />
                  • Bus company name must be lowercase
                  <br />
                  • Replace spaces with underscores (_)
                  <br />
                  • Bus number must remain exactly as shown
                  <br />
                  • Registration number must remain uppercase
                  <br />
                  • No spaces in the flag
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Fullscreen Overlay */}
      {fullscreen && (
        <div className="fullscreen-overlay" onClick={() => setFullscreen(false)}>
          <button
            className="fullscreen-close"
            onClick={(e) => {
              e.stopPropagation();
              setFullscreen(false);
            }}
          >
            ✕
          </button>
          <img
            src="/buses.png"
            alt="Evidence full screen view"
            style={{ transform: `rotate(${rotation}deg)` }}
          />
        </div>
      )}

      {/* Confetti */}
      {confetti.map((piece) => (
        <div
          key={piece.id}
          className="confetti-piece"
          style={{
            left: piece.left,
            backgroundColor: piece.color,
            animationDelay: piece.delay,
            width: piece.size,
            height: piece.size,
            borderRadius: piece.shape,
          }}
        />
      ))}
    </>
  );
}
