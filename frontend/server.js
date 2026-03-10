const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const crypto = require('crypto'); // Added for CSRF token generation

const app = express();
const PORT = 3005;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '')));

// In-memory store for CSRF Tokens mapping teamName -> token
const csrfTokens = {};

// Set up SQLite Database
const dbPath = path.resolve(__dirname, 'ctf_hub.db');
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('Error opening database ', err.message);
    } else {
        db.serialize(() => {
            // Drop old tables if they exist to force team schema update
            db.run(`DROP TABLE IF EXISTS users`);
            db.run(`DROP TABLE IF EXISTS attempts`);

            db.run(`CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT UNIQUE,
                score INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )`);

            db.run(`CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT,
                challenge_id INTEGER,
                attempts INTEGER DEFAULT 0,
                locked_until DATETIME DEFAULT NULL,
                solved BOOLEAN DEFAULT FALSE,
                UNIQUE(team_name, challenge_id)
            )`);
            console.log('Database connected and tables created/updated for teams.');
        });
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
    21: 'DAKSHH{b1g_int3g3rs_n33d_b1gg3r_st3ps}',
    // OSINT
    22: 'dakshh{075-326-3027}',
    23: 'dakshh{ditobus_4646_UY89703}',
    // Mixed
    24: 'dakshh{time_traveler}',
    25: 'dakshh{heritage_kolkata}',
    // Intro
    26: 'DAKSHH{1mp0$t3r_$p0tt3d}',
    // Rev Engg (Extended)
    27: 'DAKSHH{uds_firmware_extracted_from_can_bus}'
};

const POINTS = {
    1: 100, 2: 200, 3: 300, 4: 500,
    5: 100, 6: 300, 7: 500,
    8: 50, 9: 50, 10: 150,
    11: 100, 12: 500,
    13: 100, 14: 300, 15: 500, 16: 100,
    17: 300, 18: 500, 19: 300, 20: 300,
    21: 300, 22: 100, 23: 300,
    24: 200, 25: 100, 26: 50,
    27: 800
};

// Helper: Get team, create if not exists
const getOrCreateTeam = (teamName) => {
    return new Promise((resolve, reject) => {
        db.get(`SELECT * FROM teams WHERE team_name = ?`, [teamName], (err, row) => {
            if (err) return reject(err);
            if (row) return resolve(row);

            db.run(`INSERT INTO teams (team_name) VALUES (?)`, [teamName], function (err) {
                if (err) return reject(err);
                
                // Fetch the newly created team to get the exact created_at timestamp
                db.get(`SELECT * FROM teams WHERE id = ?`, [this.lastID], (err, newRow) => {
                    if (err) return reject(err);
                    resolve(newRow);
                });
            });
        });
    });
};

// Helper: Get or create attempt record
const getAttemptRecord = (teamName, challengeId) => {
    return new Promise((resolve, reject) => {
        db.get(`SELECT * FROM attempts WHERE team_name = ? AND challenge_id = ?`, [teamName, challengeId], (err, row) => {
            if (err) return reject(err);
            if (row) return resolve(row);

            db.run(`INSERT INTO attempts (team_name, challenge_id) VALUES (?, ?)`, [teamName, challengeId], function (err) {
                if (err) return reject(err);
                resolve({ id: this.lastID, team_name: teamName, challenge_id: challengeId, attempts: 0, locked_until: null, solved: 0 });
            });
        });
    });
};

// CSRF Token Generation Endpoint
app.get('/api/csrf-token', (req, res) => {
    const teamName = req.query.teamName;
    if (!teamName) {
        return res.status(400).json({ error: 'teamName query parameter is required' });
    }
    // Generate a secure random token
    const token = crypto.randomUUID();
    csrfTokens[teamName] = token;
    res.json({ csrfToken: token });
});

app.post('/api/submit', async (req, res) => {
    const { teamName, challengeId, flag } = req.body;
    const clientToken = req.headers['x-csrf-token'];

    if (!teamName || !challengeId || !flag) {
        return res.status(400).json({ error: 'Team name, challengeId, and flag are required.' });
    }

    // CSRF Validation
    if (!clientToken || csrfTokens[teamName] !== clientToken) {
        return res.status(403).json({ error: 'CSRF token missing or invalid. Request forbidden.' });
    }

    try {
        const team = await getOrCreateTeam(teamName);
        const record = await getAttemptRecord(teamName, challengeId);

        if (record.solved) {
            return res.json({ success: false, message: 'Your team has already solved this challenge!' });
        }

        const now = new Date();

        // Check if locked out
        if (record.locked_until && new Date(record.locked_until) > now) {
            const remTime = Math.ceil((new Date(record.locked_until) - now) / 60000);
            return res.status(429).json({ error: `You are locked out of this challenge for ${remTime} more minutes.` });
        }

        // Process Submission
        if (flag === FLAGS[challengeId] || flag === Object.values(FLAGS)[challengeId - 1]) { // Added safety check for values
            const points = POINTS[challengeId] || 100;
            
            // Bypass Anti-Cheat constraint for Intro Challenge
            if (challengeId == 26) {
                db.run(`UPDATE attempts SET solved = 1 WHERE id = ?`, [record.id]);
                db.run(`UPDATE teams SET score = score + ? WHERE team_name = ?`, [points, teamName]);
                return res.json({ success: true, message: 'Flag correct! Points awarded.' });
            }
            
            // Anti-cheat check: ensure minimum time has passed
            const minAllowedDurationMinutes = (points / 100) * 2;
            // Append 'Z' to SQLite's UTC timestamp so JS Date parses it correctly as UTC instead of local time
            const teamCreationTime = new Date(team.created_at + 'Z');
            
            // Getting the last solve time for this team to prevent dumping all flags at once.
            db.get(`SELECT MAX(locked_until) as last_solve FROM attempts WHERE team_name = ? AND solved = 1`, [teamName], (err, lastSolveRow) => {
                let baselineTime = teamCreationTime;
                
                // For simplicity, we just check against team creation. A more robust system would check the time elapsed since their previous solve.
                const timeDiffMinutes = (now - baselineTime) / 60000;

                if (timeDiffMinutes < minAllowedDurationMinutes) {
                    // Flag dump detected
                    console.log(`[ANTI-CHEAT] ${teamName} submitted flag for ${challengeId} too fast. Expected >= ${minAllowedDurationMinutes}m, took ${timeDiffMinutes.toFixed(2)}m.`);
                    return res.status(403).json({ error: 'Anti-cheat triggered: Flag submission speed too fast. Please allow time for natural progression.' });
                }

                // Correct flag
                db.run(`UPDATE attempts SET solved = 1 WHERE id = ?`, [record.id]);
                db.run(`UPDATE teams SET score = score + ? WHERE team_name = ?`, [points, teamName]);
                return res.json({ success: true, message: 'Flag correct! Points awarded.' });
            });
            return; // Wait for callback
        } else {
            // Wrong flag
            let newAttempts = record.attempts + 1;
            let lockedUntil = null;
            let penaltyApplied = false;
            
            if (challengeId == 26) {
                db.run(`UPDATE attempts SET attempts = ? WHERE id = ?`, [newAttempts, record.id]);
                return res.json({ success: false, message: 'Incorrect flag. Keep trying!' });
            }
            
            let message = `Incorrect flag. You have used ${newAttempts}/10 attempts.`;

            if (newAttempts >= 10) {
                // Lockout for 30 minutes
                lockedUntil = new Date(now.getTime() + 30 * 60000).toISOString();
                newAttempts = 0; // reset attempts after lockout
                
                // Apply 10 point deduction penalty for brute forcing
                db.run(`UPDATE teams SET score = MAX(0, score - 10) WHERE team_name = ?`, [teamName]);
                penaltyApplied = true;
                
                message = `Incorrect flag limit reached. Locked out for 30 minutes. Penalty applied: -10 points.`;
            }

            db.run(`UPDATE attempts SET attempts = ?, locked_until = ? WHERE id = ?`, [newAttempts, lockedUntil, record.id]);
            return res.json({ success: false, penaltyApplied, message });
        }
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal server error.' });
    }
});

app.get('/api/leaderboard', (req, res) => {
    const query = `
        SELECT t.team_name as username, t.score, COUNT(a.id) as solved_count
        FROM teams t
        LEFT JOIN attempts a ON t.team_name = a.team_name AND a.solved = 1
        GROUP BY t.team_name
        ORDER BY t.score DESC, solved_count DESC
        LIMIT 10
    `;
    db.all(query, (err, rows) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to fetch leaderboard' });
        }
        res.json({ leaderboard: rows, totalChallenges: Object.keys(FLAGS).length });
    });
});

app.get('/api/leaderboard/full', (req, res) => {
    const query = `
        SELECT t.team_name as username, t.score, COUNT(a.id) as solved_count
        FROM teams t
        LEFT JOIN attempts a ON t.team_name = a.team_name AND a.solved = 1
        GROUP BY t.team_name
        ORDER BY t.score DESC, solved_count DESC
    `;
    db.all(query, (err, rows) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to fetch full leaderboard' });
        }
        res.json({ leaderboard: rows, totalChallenges: Object.keys(FLAGS).length });
    });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`CTF Base Server running on port ${PORT}`);
});
