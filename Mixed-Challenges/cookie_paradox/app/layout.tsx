import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "Dakshh Vault",
    description: "Secure Vault Access",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body>
                <div className="scanline"></div>
                {children}
            </body>
        </html>
    );
}
