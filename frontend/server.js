const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const PORT = 3005;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '')));

// Set up SQLite Database
const dbPath = path.resolve(__dirname, 'ctf_hub.db');
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('Error opening database ', err.message);
    } else {
        db.run(`CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            score INTEGER DEFAULT 0
        )`);

        db.run(`CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            challenge_id INTEGER,
            attempts INTEGER DEFAULT 0,
            locked_until DATETIME DEFAULT NULL,
            solved BOOLEAN DEFAULT FALSE,
            UNIQUE(username, challenge_id)
        )`);
        console.log('Database connected and tables created.');
    }
});

const FLAGS = {
    1: 'DAKSHH{sus_in_the_dom}',
    2: 'DAKSHH{batman_needs_access_control}',
    3: 'DAKSHH{stateside_man_in_the_middle}',
    4: 'DAKSHH{ecorp_archive_traversal_bypassed}'
};

const POINTS = {
    1: 100,
    2: 200,
    3: 300,
    4: 500
};

// Helper: Get user, create if not exists
const getOrCreateUser = (username) => {
    return new Promise((resolve, reject) => {
        db.get(`SELECT * FROM users WHERE username = ?`, [username], (err, row) => {
            if (err) return reject(err);
            if (row) return resolve(row);

            db.run(`INSERT INTO users (username) VALUES (?)`, [username], function (err) {
                if (err) return reject(err);
                resolve({ id: this.lastID, username, score: 0 });
            });
        });
    });
};

// Helper: Get or create attempt record
const getAttemptRecord = (username, challengeId) => {
    return new Promise((resolve, reject) => {
        db.get(`SELECT * FROM attempts WHERE username = ? AND challenge_id = ?`, [username, challengeId], (err, row) => {
            if (err) return reject(err);
            if (row) return resolve(row);

            db.run(`INSERT INTO attempts (username, challenge_id) VALUES (?, ?)`, [username, challengeId], function (err) {
                if (err) return reject(err);
                resolve({ id: this.lastID, username, challenge_id: challengeId, attempts: 0, locked_until: null, solved: 0 });
            });
        });
    });
};

app.post('/api/submit', async (req, res) => {
    const { username, challengeId, flag } = req.body;

    if (!username || !challengeId || !flag) {
        return res.status(400).json({ error: 'Username, challengeId, and flag are required.' });
    }

    try {
        await getOrCreateUser(username);
        const record = await getAttemptRecord(username, challengeId);

        if (record.solved) {
            return res.json({ success: false, message: 'You have already solved this challenge!' });
        }

        const now = new Date();

        // Check if locked out
        if (record.locked_until && new Date(record.locked_until) > now) {
            const remTime = Math.ceil((new Date(record.locked_until) - now) / 60000);
            return res.status(429).json({ error: `You are locked out of this challenge for ${remTime} more minutes.` });
        }

        // Process Submission
        if (flag === FLAGS[challengeId]) {
            // Correct flag
            db.run(`UPDATE attempts SET solved = 1 WHERE id = ?`, [record.id]);
            db.run(`UPDATE users SET score = score + ? WHERE username = ?`, [POINTS[challengeId], username]);
            return res.json({ success: true, message: 'Flag correct! Points awarded.' });
        } else {
            // Wrong flag
            let newAttempts = record.attempts + 1;
            let lockedUntil = null;
            let message = `Incorrect flag. You have used ${newAttempts}/10 attempts.`;

            if (newAttempts >= 10) {
                // Lockout for 30 minutes
                lockedUntil = new Date(now.getTime() + 30 * 60000).toISOString();
                newAttempts = 0; // reset attempts after lockout
                message = `Incorrect flag. Max attempts reached. Locked out for 30 minutes.`;
            }

            db.run(`UPDATE attempts SET attempts = ?, locked_until = ? WHERE id = ?`, [newAttempts, lockedUntil, record.id]);
            return res.json({ success: false, message });
        }
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal server error.' });
    }
});

app.get('/api/leaderboard', (req, res) => {
    db.all(`SELECT username, score FROM users ORDER BY score DESC LIMIT 10`, (err, rows) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to fetch leaderboard' });
        }
        res.json(rows);
    });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`CTF Base Server running on port ${PORT}`);
});
