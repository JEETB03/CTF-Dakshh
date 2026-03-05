const express = require('express');
const app = express();
const port = 3000;

app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.send(`
    <html>
    <head>
        <title>Polus Crew Portal</title>
        <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Share Tech Mono', monospace; background-color: #0b0c10; color: #45a29e; padding: 0; margin: 0; }
            .bg-stars { background: url('https://www.transparenttextures.com/patterns/stardust.png') repeat; height: 100vh; padding: 40px 20px; }
            .container { max-width: 700px; margin: 0 auto; background: rgba(31, 40, 51, 0.9); border: 2px solid #66fcf1; border-radius: 10px; padding: 30px; box-shadow: 0 0 20px #66fcf1; }
            h1 { text-align: center; color: #c5c6c7; font-size: 2.5em; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 2px; }
            p { text-align: center; font-size: 1.1em; color: #c5c6c7; margin-bottom: 30px; }
            input[type="text"] { width: 100%; box-sizing: border-box; padding: 15px; background: #0b0c10; color: #66fcf1; border: 1px solid #45a29e; font-family: 'Share Tech Mono'; font-size: 1.1em; margin-bottom: 15px; border-radius: 5px; }
            input[type="text"]:focus { outline: none; border-color: #66fcf1; box-shadow: 0 0 10px rgba(102, 252, 241, 0.5); }
            button { width: 100%; padding: 15px; background: #45a29e; color: #0b0c10; border: none; font-family: 'Share Tech Mono'; font-size: 1.2em; font-weight: bold; cursor: pointer; border-radius: 5px; transition: 0.2s; text-transform: uppercase; }
            button:hover { background: #66fcf1; box-shadow: 0 0 10px #66fcf1; }
            .report-section { margin-top: 40px; padding-top: 20px; border-top: 1px dashed #45a29e; }
            .report-section h2 { color: #f0f0f0; font-size: 1.5em; text-align: center; }
            .footer { margin-top: 30px; font-size: 0.85em; color: #555; text-align: center; }
            .alert { color: #ff3b3b; font-weight: bold; text-align: center; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="bg-stars">
            <div class="container">
                <h1>Polus Crew Terminal</h1>
                <p>Submit your anonymous tasks and feedback to mission control.</p>
                <form action="/feedback" method="GET">
                    <input type="text" name="msg" placeholder="Enter message logging..." required>
                    <button type="submit">Transmit Log</button>
                </form>
                
                <div class="report-section">
                    <h2>Admin Intervention Required?</h2>
                    <p style="font-size: 0.9em; margin-bottom: 15px;">If you suspect a crewmate's log contains malicious payloads, report the exact URL transmission below:</p>
                    <form action="/report" method="POST">
                        <input type="text" name="url" placeholder="http://app:3000/feedback?msg=..." required>
                        <button type="submit" style="background: #ff3b3b; color: white;">Report URL</button>
                    </form>
                </div>
                
                <div class="footer">
                    <p>"Hello friend... hello friend? That's lame."</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    `);
});

app.get('/feedback', (req, res) => {
    let msg = req.query.msg || '';

    // The filter
    const blockedKeywords = ['script', 'alert', 'onerror'];
    for (let word of blockedKeywords) {
        if (msg.toLowerCase().includes(word)) {
            return res.send("Blocked: Malicious input detected.");
        }
    }

    res.send(`
    <html>
    <head>
        <title>Log Received</title>
        <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Share Tech Mono', monospace; background-color: #0b0c10; color: #45a29e; padding: 0; margin: 0; }
            .bg-stars { background: url('https://www.transparenttextures.com/patterns/stardust.png') repeat; height: 100vh; padding: 40px 20px; }
            .container { max-width: 700px; margin: 0 auto; background: rgba(31, 40, 51, 0.9); border: 2px solid #66fcf1; border-radius: 10px; padding: 30px; box-shadow: 0 0 20px #66fcf1; text-align: center; }
            h1 { color: #66fcf1; margin-bottom: 20px; }
            .log-box { background: #0b0c10; padding: 20px; border: 1px solid #45a29e; border-radius: 5px; color: #c5c6c7; word-wrap: break-word; text-align: left; }
            a { display: inline-block; margin-top: 30px; color: #66fcf1; text-decoration: none; border: 1px solid #66fcf1; padding: 10px 20px; border-radius: 5px; transition: 0.2s; }
            a:hover { background: #66fcf1; color: #0b0c10; }
            .footer { margin-top: 30px; font-size: 0.85em; color: #555; }
        </style>
    </head>
    <body>
        <div class="bg-stars">
            <div class="container">
                <h1>Log Transmission Successful</h1>
                <!-- sanitize later... seems kinda sus -->
                <div class="log-box">
                    <strong>Message:</strong><br><br>
                    ${msg}
                </div>
                <a href="/">Return to Map</a>
                <div class="footer">
                    <p>"Hello friend... hello friend? That's lame."</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    `);
});

app.post('/report', async (req, res) => {
    let url = req.body.url;
    if (!url || !url.startsWith('http')) {
        return res.send("Invalid URL.");
    }
    try {
        const fetch = (await import('node-fetch')).default;
        // Make a request to the bot container
        const response = await fetch('http://bot:3001/visit', {
            method: 'POST',
            body: new URLSearchParams({ 'url': url }),
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        const text = await response.text();
        res.send(text + ' <a href="/">Go back</a>');
    } catch (e) {
        console.error(e);
        res.send("Failed to contact admin bot. <a href='/'>Go back</a>");
    }
});

app.get('/flag', (req, res) => {
    // Check if the user is the admin (bot) by checking cookies
    if (req.headers.cookie && req.headers.cookie.includes('admin=true')) {
        res.send("DAKSHH{sus_in_the_dom}");
    } else {
        res.status(403).send("Access Denied: You are not an administrator.");
    }
});

app.listen(port, '0.0.0.0', () => {
    console.log("Crew portal running on port " + port);
});
