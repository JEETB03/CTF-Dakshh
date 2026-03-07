"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function OsintChallenge() {
    const router = useRouter();
    const [solved, setSolved] = useState(false);

    if (solved) {
        return (
            <div style={{ marginTop: "20px" }}>
                <p className="text-green">System fully breached. All objectives completed.</p>
                <button onClick={() => router.push("/dashboard")} className="btn" style={{ marginTop: "10px", width: "100%" }}>Return to Dashboard</button>
            </div>
        );
    }

    return (
        <div className="vault-box" style={{ marginTop: "20px" }}>
            <p>You have successfully infiltrated the main vault.</p>
            <p>Now, decrypt this intercepted message (Caesar Cipher).</p>
            <p><em>Hint: The shift key has been hidden where the robots aren't allowed...</em></p>
            <div className="terminal-container" style={{ padding: "10px", margin: "10px 0", border: '1px dashed #0f0' }}>
                <code>khulwdjh_nrondwd</code>
            </div>
            <button onClick={() => router.push("/dashboard")} className="btn" style={{ marginTop: "10px", width: "100%" }}>Return to Dashboard</button>
        </div>
    );
}
