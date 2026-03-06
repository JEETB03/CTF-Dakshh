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
    // Web
    1: 'DAKSHH{sus_in_the_dom}',
    2: 'DAKSHH{batman_needs_access_control}',
    3: 'DAKSHH{stateside_man_in_the_middle}',
    4: 'DAKSHH{ecorp_archive_traversal_bypassed}',
    // Crypto
    5: 'DAKSHH{n30_f0und_th3_r3d_p1ll_x0r}',
    6: 'DAKSHH{3l3m3nt4ry_my_d34r_w4ts0n_0tp}',
    7: 'DAKSHH{n0_c0rp0_n3tw0rk_1s_s4f3_fr0m_rs4}',
    // Misc
    8: 'flag{satellite_signal_restored}',
    9: 'flag{qr_codes_never_lie}',
    10: 'flag{training_data_poisoned}',
    // Rev Engg
    11: 'DAKSHH{H1DD3N_C0D3}',
    12: 'DAKSHH{7h15_f14g_15_v3ry_v3ry_l0ng_4nd_1_h0p3_th3r3_4r3_n0_7yp0}',
    // Web (Extended)
    13: 'DAKSHH{sqli_3asy_byP4ss_2026}',
    14: 'DAKSHH{w4f_byp4ss_w1th0ut_c0mp4r1s0ns}',
    15: 'DAKSHH{un1c0d3_n0rm4l1z4t10n_sqli_ph4nt0m}',
    16: 'DAKSHH{h1nglish_hunt_3asy}',
    17: 'DAKSHH{css_gh0st_m3d1um}',
    18: 'DAKSHH{css_gh0st_m3d1um_h4rd_fr4gm3nt_b0ss}',
    19: 'DAKSHH{GrEaT_yOu_ReCoVeReD_tHiS_sItE_2026}',
    20: 'DAKSHH{h0st_h34d3r_p01s0n1ng_f0r_t4h_w1n}',
    // Crypto (Extended)
    21: 'DAKSHH{b1g_int3g3rs_n33d_b1gg3r_st3ps}'
};

const POINTS = {
    1: 100, 2: 200, 3: 300, 4: 500,
    5: 100, 6: 300, 7: 500,
    8: 50, 9: 50, 10: 150,
    11: 100, 12: 500,
    13: 100, 14: 300, 15: 500, 16: 100,
    17: 300, 18: 500, 19: 300, 20: 300,
    21: 300
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

app.get('/api/leaderboard/full', (req, res) => {
    const query = `
        SELECT u.username, u.score, COUNT(a.id) as solved_count
        FROM users u
        LEFT JOIN attempts a ON u.username = a.username AND a.solved = 1
        GROUP BY u.username
        ORDER BY u.score DESC, solved_count DESC
    `;
    db.all(query, (err, rows) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to fetch full leaderboard' });
        }
        res.json(rows);
    });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`CTF Base Server running on port ${PORT}`);
});
