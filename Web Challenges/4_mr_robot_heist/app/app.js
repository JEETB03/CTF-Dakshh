const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// The flag is placed at the project root for local development, docker will put it at /flag.txt
const FLAG_PATH = path.join(__dirname, 'flag.txt');
fs.writeFileSync(FLAG_PATH, 'DAKSHH{ecorp_archive_traversal_bypassed}');

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/api/read', (req, res) => {
    let fileParam = req.query.file;

    if (!fileParam) {
        return res.status(400).json({ error: 'No file specified.' });
    }

    // WAF Logic 1: Basic Path Traversal Prevention
    // The developer tried to be smart and replace '../' globally
    let cleanFile = fileParam.replace(/\.\.\//g, '');

    // WAF Logic 2: Force extension to .txt to prevent reading binaries/scripts
    // But if the attacker aims for '/flag.txt' directly, this might accidentally help them if they reach the root.
    if (!cleanFile.endsWith('.txt')) {
        cleanFile += '.txt';
    }

    // WAF Logic 3: URL Decode to prevent basic URL encoded bypasses (%2e%2e%2f)
    // However, if the attacker DOUBLE URL encodes (%252e%252e%252f), it bypasses this single decode, 
    // and `path.resolve` handles the second layer implicitly!
    cleanFile = decodeURIComponent(cleanFile);

    // Secure Document Directory
    const baseDir = path.join(__dirname, 'documents');

    // Resolve the final absolute path (e.g. going up from __dirname/documents to __dirname)
    const finalPath = path.resolve(baseDir, cleanFile);

    console.log(`[E-Corp Archival System] Attempting to read: ${finalPath}`);

    // Check if the file actually exists
    if (!fs.existsSync(finalPath)) {
        return res.status(404).json({ error: 'File not found in archives.' });
    }

    // Read and return the file content
    try {
        const content = fs.readFileSync(finalPath, 'utf8');
        res.json({ success: true, content: content, path: finalPath });
    } catch (err) {
        res.status(500).json({ error: 'Internal Archive Error.' });
    }
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`E-Corp Archival System running on port ${PORT}`);

    // Ensure the documents directory exists with dummy files
    const docsDir = path.join(__dirname, 'documents');
    if (!fs.existsSync(docsDir)) {
        fs.mkdirSync(docsDir);
        fs.writeFileSync(path.join(docsDir, 'memo_501.txt'), 'Confidential Memo: Server upgrades are delayed until Q3.');
        fs.writeFileSync(path.join(docsDir, 'financials_Q2.txt'), 'Q2 Financials: Revenue is up 14%, but proxy server costs are escalating.');
        fs.writeFileSync(path.join(docsDir, 'fsociety_note.txt'), 'We see you. Encoding is the key. They only peel back one layer of the onion.');
    }
});
