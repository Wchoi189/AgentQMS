const puppeteer = require('puppeteer');

async function capturePage() {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();

        // Capture console messages and errors
        page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
        page.on('pageerror', error => console.log('PAGE ERROR:', error.message));

        const url = process.argv[2] || 'http://localhost:8501/schema_inference';
        console.log(`Navigating to ${url}`);
        await page.goto(url, {
            waitUntil: 'networkidle2',
            timeout: 30000
        });

        // Wait a bit for Streamlit to render
        await new Promise(resolve => setTimeout(resolve, 3000));

        // Get all text content
        const bodyText = await page.evaluate(() => {
            return document.body.innerText;
        });

        console.log('\n=== PAGE CONTENT ===\n');
        console.log(bodyText);

        // Look for error messages specifically
        const errors = await page.evaluate(() => {
            const errorElements = Array.from(document.querySelectorAll('[data-testid="stException"], .stException, [class*="error"]'));
            return errorElements.map(el => el.innerText).filter(text => text.length > 0);
        });

        if (errors.length > 0) {
            console.log('\n=== ERRORS FOUND ===\n');
            errors.forEach(error => console.log(error));
        }

    } catch (error) {
        console.error('Error:', error.message);
    } finally {
        await browser.close();
    }
}

capturePage();
