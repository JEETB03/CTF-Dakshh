import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Shadow Lens — Holiday Bus Investigation",
  description: "Act as a digital investigator solving real-world clues using OSINT techniques. Investigate the holiday bus image and identify key details.",
  keywords: ["CTF", "OSINT", "Capture The Flag", "Investigation", "Bus", "Challenge"],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {/* Navbar */}
        <nav className="navbar">
          <a href="/" className="navbar-brand">
            <div className="navbar-logo">🕵️</div>
            <div className="navbar-title">
              Shadow <span>Lens</span>
            </div>
          </a>
          <div className="navbar-status">
            🏆 Points - 600
          </div>
        </nav>
        {children}
      </body>
    </html>
  );
}
