const puppeteer = require('puppeteer');

const url = process.argv[2];

if (!url) {
    console.error('Usage: node bot.js <url>');
    process.exit(1);
}

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function visit() {
    console.log(`[+] Bot started visiting: ${url}`);
    let browser;
    try {
        browser = await puppeteer.launch({
            headless: "new",
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu'
            ]
        });

        const page = await browser.newPage();

        // Setting the admin cookie BEFORE visiting the target domain
        // In a real scenario, the domain should match the hosting domain
        await page.setCookie({
            name: '_ga',
            value: 'YWRtaW5fY29va2llc19pc192ZXJ5X3Rhc3R5',
            domain: '127.0.0.1', // IMPORTANT: This needs to match the host in the URL
            path: '/',
            httpOnly: false,
            secure: false
        });

        // Add a second cookie just to show the flag format
        await page.setCookie({
            name: 'flag',
            value: 'DAKSHH{GrEaT_yOu_ReCoVeReD_tHiS_sItE_2026}',
            domain: '127.0.0.1',
            path: '/',
            httpOnly: false,
            secure: false
        });

        console.log('[+] Cookies set successfully');

        // Go to the URL submitted by the user
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 5000 });
        console.log('[+] URL loaded');

        // Wait a bit for any XSS payload to execute and exfiltrate data
        await sleep(3000);

        console.log('[+] Done visiting');

    } catch (e) {
        console.error('[-] Error visiting:', e.message);
    } finally {
        if (browser) {
            await browser.close();
            console.log('[+] Browser closed');
        }
    }
}

visit();
