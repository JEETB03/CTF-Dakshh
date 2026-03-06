"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function VaultQuestion() {
    return (
        <div className="vault-wrapper">
            <Card className="ctf-card vault-card">
                <CardHeader className="ctf-card-header">
                    <div className="vault-icon">🔓</div>
                    <CardTitle className="ctf-card-title vault-title">
                        Time Vault Unlocked
                    </CardTitle>
                </CardHeader>
                <CardContent className="ctf-card-content">
                    <div className="vault-question-block">
                        <p className="vault-question">
                            Dakshh is being hosted again at Heritage Institute.
                            <br />
                            <strong>After how many years is Dakshh being hosted again?</strong>
                            <br />
                            <br />
                            <strong>Decode the encrypted answer below to proceed.</strong>
                        </p>
                    </div>

                    <div className="cipher-block">
                        <div className="cipher-label">Encoded Answer:</div>
                        <div className="cipher-value">crvn_cajnuna</div>
                    </div>

                    <p className="cipher-hint">
                        💡 Hint: The organizers like classic encryption methods. The number of years might be the key...
                    </p>

                    <p className="vault-submit-note">
                        🚩 Decode the answer and submit it as the flag on the CTF platform.
                    </p>
                </CardContent>
            </Card>
        </div>
    );
}
