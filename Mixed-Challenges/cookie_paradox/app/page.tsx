"use client";

import { useEffect, useState } from "react";
import { setCookie } from "../utils/cookie";
import { useRouter } from "next/navigation";

export default function Home() {
    const router = useRouter();
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
        // Clear any existing session so every user starts fresh
        setCookie("auth_token", "", -1);
    }, []);

    const handleGuestLogin = () => {
        const tokenStr = `guest:0`;
        const encodedToken = btoa(tokenStr);

        setCookie("auth_token", encodedToken, 1);
        router.push("/dashboard");
    };

    const handleAdminLogin = () => {
        alert("Connection to auth server failed. Error 0x88fA. Please use Guest Login.");
    };

    if (!mounted) return null; // Avoid SSR mismatch

    return (
        <div className="terminal-container">
            <h1 className="glitch-text">Dakshh Digital Vault</h1>
            <p>Welcome to Dakshh Vault.</p>
            <p>Only authorized administrators can access the secure vault.</p>
            <p>Guests may explore the system but cannot access protected files.</p>

            <div className="login-form">
                <h3>Admin Login</h3>
                <input type="text" id="username" placeholder="Username" autoComplete="off" />
                <input type="password" id="password" placeholder="Password" autoComplete="off" />
                <button className="btn" onClick={handleAdminLogin}>Login</button>
            </div>

            <div style={{ textAlign: "center", marginTop: "30px" }}>
                <p>--- OR ---</p>
                <button className="btn" onClick={handleGuestLogin}>Continue as Guest</button>
            </div>
        </div>
    );
}
