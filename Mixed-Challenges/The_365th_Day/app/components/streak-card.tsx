"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";

interface StreakCardProps {
    onVaultUnlocked: () => void;
}

export default function StreakCard({ onVaultUnlocked }: StreakCardProps) {
    const [streak, setStreak] = useState<number>(0);
    const [message, setMessage] = useState<string | null>(null);
    const [messageType, setMessageType] = useState<"error" | "success">("error");
    const [mounted, setMounted] = useState(false);
    const [animateStreak, setAnimateStreak] = useState(false);

    useEffect(() => {
        setMounted(true);
        updateStreak();
    }, []);

    const updateStreak = () => {
        // Always reset to 1 on every page load so each visitor starts fresh.
        // This prevents one user's solved state from leaking to the next user.
        // Players must manually edit localStorage and then click "Claim Reward".
        const now = Date.now();
        localStorage.setItem("login_streak", "1");
        localStorage.setItem("last_login", now.toString());
        setStreak(1);
    };

    const handleClaimReward = () => {
        // Re-read localStorage each time to pick up manual edits
        const currentStreak = parseInt(localStorage.getItem("login_streak") || "0");
        setStreak(currentStreak);

        setAnimateStreak(true);
        setTimeout(() => setAnimateStreak(false), 600);

        if (currentStreak >= 365) {
            setMessage(null);
            setMessageType("success");
            onVaultUnlocked();
        } else {
            setMessageType("error");
            setMessage(
                `⏳ Time anomaly detected.\n\nYou need 365 login streak to unlock the Time Vault.\n\nCurrent streak: ${currentStreak}`
            );
        }
    };

    if (!mounted) return null;

    return (
        <div className="streak-card-wrapper">
            <Card className="ctf-card">
                <CardHeader className="ctf-card-header">
                    <div className="streak-icon">🕐</div>
                    <CardTitle className="ctf-card-title">Daily Login Streak</CardTitle>
                </CardHeader>
                <CardContent className="ctf-card-content">
                    <div className="streak-display">
                        <span className="streak-label">Current Streak</span>
                        <div className={`streak-number ${animateStreak ? "streak-pulse" : ""}`}>
                            {streak}
                            <span className="streak-unit">days</span>
                        </div>
                    </div>

                    <div className="streak-progress-bar">
                        <div
                            className="streak-progress-fill"
                            style={{ width: `${Math.min((streak / 365) * 100, 100)}%` }}
                        />
                        <span className="streak-progress-text">{streak} / 365</span>
                    </div>

                    <Button
                        onClick={handleClaimReward}
                        className="claim-button"
                    >
                        <span className="claim-button-text">⚡ Claim Reward</span>
                    </Button>

                    {message && (
                        <Alert className={`ctf-alert ${messageType === "error" ? "ctf-alert-warning" : "ctf-alert-success"}`}>
                            <AlertDescription className="ctf-alert-desc">
                                {message.split("\n").map((line, i) => (
                                    <span key={i}>
                                        {line}
                                        {i < message.split("\n").length - 1 && <br />}
                                    </span>
                                ))}
                            </AlertDescription>
                        </Alert>
                    )}

                      <div className="text-xs text-zinc-600 mt-4 italic font-mono opacity-50">
                        &quot;Time travelers don&apos;t wait a year… they rewrite history.&quot;
                        <br />— The 365th Day
                      </div>
                </CardContent>
            </Card>
        </div>
    );
}
