import { cookies } from "next/headers";
import Link from "next/link";
import { redirect } from "next/navigation";
import OsintChallenge from "./OsintChallenge";

export default async function Vault() {
    const cookieStore = await cookies();
    const token = cookieStore.get("auth_token")?.value;

    if (!token) {
        redirect("/");
    }

    try {
        const decoded = Buffer.from(token, 'base64').toString('utf-8');
        const [username, admin] = decoded.split(":");

        if (admin !== "1") {
            return (
                <div className="terminal-container" id="vault-content">
                    <h2>ACCESS LEVEL: GUEST</h2>
                    <div className="text-red">Vault Access Denied.</div>
                    <p>Only administrators can access this area.</p>
                    <Link href="/dashboard" className="btn" style={{ display: 'inline-block', marginTop: '10px', textDecoration: 'none' }}>Return</Link>
                </div>
            );
        }

        // Admin Access Allowed
        return (
            <div className="terminal-container" id="vault-content">
                <div className="glitch-text text-green">ACCESS LEVEL: ADMIN</div>
                <div className="text-green blink">AUTHORIZATION: VERIFIED</div>
                <br />
                <div className="typing-anim" style={{ animation: 'none', borderRight: 'none', whiteSpace: 'normal' }}>Vault Files Decrypted Successfully.</div>
                <br />
                {username === "deadpool" ? (
                    <div className="vault-box border-red">
                        <h3 className="text-red">Secret Deadpool Easter Egg</h3>
                        <p>Oh yeah! You found my secret stash! Maximum Effort!</p>
                        <p>Hmm, I seem to have misplaced the flag though. Submit "maximum_effort_cookie_hacker" wrapped in the standard flag format to your CTF platform to claim your prize!</p>
                    </div>
                ) : (
                    <></>
                )}
                <OsintChallenge />
            </div>
        );

    } catch (e) {
        return (
            <div className="terminal-container" id="vault-content">
                <div className="glitch-text text-red">CRITICAL ERROR</div>
                <p>Malformed base-64 payload format.</p>
                <Link href="/dashboard" className="btn" style={{ display: 'inline-block', marginTop: '10px', textDecoration: 'none' }}>Return to Dashboard</Link>
            </div>
        );
    }
}
