"use client";

import { useEffect, useState } from "react";
import { getCookie, setCookie } from "../../utils/cookie";
import { useRouter } from "next/navigation";

export default function Dashboard() {
    const router = useRouter();
    const [mounted, setMounted] = useState(false);
    const [user, setUser] = useState("...");
    const [isAdmin, setIsAdmin] = useState(false);

    useEffect(() => {
        setMounted(true);
        const token = getCookie("auth_token");
        if (!token) {
            router.push("/");
            return;
        }

        try {
            const decoded = atob(token);
            const [username, admin] = decoded.split(":");
            setUser(username || "Unknown");
            setIsAdmin(admin === "1");
        } catch (e) {
            console.error("Cookie parsing failed", e);
            setCookie("auth_token", "", -1);
            router.push("/");
        }
    }, [router]);

    const handleLogout = () => {
        setCookie("auth_token", "", -1);
        router.push("/");
    };

    const handleEnterVault = () => {
        router.push("/vault");
    };

    if (!mounted) return null;

    return (
        <div className="terminal-container">
            <h2>Dashboard</h2>
            <div style={{ marginBottom: "20px" }}>
                <p><strong>Logged in as:</strong> <span id="logged-in-user" className="text-green">{user}</span></p>
                <p>
                    <strong>Access Level:</strong>
                    <span id="access-level" className={isAdmin ? "text-green" : "text-red"}>
                        {isAdmin ? "Administrator" : "Guest"}
                    </span>
                </p>
            </div>

            <button className="btn" onClick={handleEnterVault}>Enter Vault</button>

            <button className="btn" onClick={handleLogout} style={{ marginTop: "20px", display: "block" }}>Logout</button>
        </div>
    );
}
