const express = require('express');
const puppeteer = require('puppeteer');
const app = express();
const port = 3001;

app.use(express.urlencoded({ extended: true }));

app.post('/visit', async (req, res) => {
    const url = req.body.url;
    if (!url || !url.startsWith('http://localhost:3000')) {
        return res.send("Bot only visits http://localhost:3000 URLs.");
    }

    try {
        const browser = await puppeteer.launch({
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
            executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || null
        });
        const page = await browser.newPage();

        await page.setCookie({
            name: 'admin',
            value: 'true',
            domain: 'app',
            path: '/',
            httpOnly: false
        });

        await page.goto(url, { waitUntil: 'networkidle2', timeout: 5000 });
        await new Promise(resolve => setTimeout(resolve, 2000));
        await browser.close();
        res.send("Admin visited the URL.");
    } catch (e) {
        console.error(e);
        res.send("Bot error.");
    }
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Bot listening on port ${port}`);
});
