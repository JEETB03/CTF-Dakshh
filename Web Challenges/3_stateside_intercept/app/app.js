const express = require('express');
const crypto = require('crypto');
const app = express();
const port = 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

const SECRET = crypto.randomBytes(32).toString('hex');

function base64url(source) {
    let encodedSource = Buffer.from(source).toString('base64');
    encodedSource = encodedSource.replace(/=+$/, '');
    encodedSource = encodedSource.replace(/\+/g, '-');
    encodedSource = encodedSource.replace(/\//g, '_');
    return encodedSource;
}

function createToken(payload) {
    const header = { alg: "HS256", typ: "JWT" };
    const encodedHeader = base64url(JSON.stringify(header));
    const encodedPayload = base64url(JSON.stringify(payload));

    const signatureInput = `${encodedHeader}.${encodedPayload}`;
    const signature = crypto.createHmac('sha256', SECRET).update(signatureInput).digest('base64url');

    return `${signatureInput}.${signature}`;
}

function verifyToken(token) {
    try {
        const parts = token.split('.');
        if (parts.length !== 3 && parts.length !== 2) return null;

        const header = JSON.parse(Buffer.from(parts[0], 'base64url').toString('utf8'));
        const payload = JSON.parse(Buffer.from(parts[1], 'base64url').toString('utf8'));
        const signature = parts[2] || '';

        // Vulnerability: alg: none
        if (header.alg === 'none') {
            return payload; // Signature check bypassed!
        }

        if (parts.length !== 3) return null;

        const signatureInput = `${parts[0]}.${parts[1]}`;
        const expectedSignature = crypto.createHmac('sha256', SECRET).update(signatureInput).digest('base64url');

        if (signature === expectedSignature) {
            return payload;
        }
    } catch (e) {
        return null;
    }
    return null;
}

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/login.html');
});

// Mock Database for Dashboard
const songs = [
    { title: "Man in the Middle", artist: "fsociety", color: "#1e3264", icon: "🎵" },
    { title: "Stateside", artist: "A.L.", color: "#450a0a", icon: "🎸" },
    { title: "Null Byte", artist: "H4X0R", color: "#003300", icon: "🎹" },
    { title: "JSON Web Tokin'", artist: "Crypto Kids", color: "#330033", icon: "🎷" },
    { title: "The Alderson Loop", artist: "Evil Corp", color: "#333300", icon: "🎧" }
];

app.get('/api/songs', (req, res) => {
    const authHeader = req.headers['authorization'];
    if (!authHeader) return res.status(401).json({ error: "Missing token" });

    const token = authHeader.split(' ')[1];
    const decoded = verifyToken(token);

    if (!decoded) return res.status(401).json({ error: "Invalid token" });

    // Both users and admins can see songs
    res.json(songs);
});

app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    if (username === 'elliot' && password === 'mrrobot') {
        const token = createToken({ user: username, role: "user" });
        return res.json({ token: token, message: "Login successful. Save this token to access the /api/admin endpoint. Hint: we verify your role through the token." });
    }
    return res.status(401).json({ error: "Invalid credentials" });
});

app.get('/api/admin', (req, res) => {
    const authHeader = req.headers['authorization'];
    if (!authHeader) return res.status(401).send("Missing Authorization Header. <!-- encryption is expensive... maybe later -->");

    const token = authHeader.split(' ')[1];
    if (!token) return res.status(401).send("Missing token");

    const decoded = verifyToken(token);
    if (!decoded) {
        return res.status(401).send("Invalid token signature.");
    }
    if (decoded && decoded.role === 'admin') {
        res.send("Welcome admin. Flag: DAKSHH{stateside_man_in_the_middle}");
    } else {
        res.status(403).send(`Access Denied: Admin role required. You are logged as ${decoded.role}`);
    }
});

app.listen(port, '0.0.0.0', () => {
    console.log("Stateside Radio API listening on port " + port);
});
