/**
 * Check Streamlit pages for errors using Puppeteer
 */

const puppeteer = require('puppeteer');

const pages = [
    { name: 'Inference Schema', url: 'http://localhost:8501/2_schema_inference' },
    { name: 'Schema Analysis', url: 'http://localhost:8501/3_schema_analysis' },
    { name: 'Analysis', url: 'http://localhost:8501/3_📈_Analysis' },
    { name: 'Schema Advanced Analysis', url: 'http://localhost:8501/4_schema_advanced_analysis' },
    { name: 'Proof of Concept', url: 'http://localhost:8501/proof_of_concept' },
    { name: 'Schema Data Explorer', url: 'http://localhost:8501/schema_data_explorer' },
    { name: 'Test Data Binding', url: 'http://localhost:8501/test_data_binding' },
];

async function checkPage(page, pageInfo) {
    const errors = [];
    const consoleMessages = [];

    // Capture console messages
    page.on('console', msg => {
        const text = msg.text();
        consoleMessages.push({ type: msg.type(), text });
        if (msg.type() === 'error') {
            errors.push(text);
        }
    });

    // Capture page errors
    page.on('pageerror', error => {
        errors.push(error.message);
    });

    try {
        console.log(`\n${'='.repeat(60)}`);
        console.log(`Checking: ${pageInfo.name}`);
        console.log(`URL: ${pageInfo.url}`);
        console.log('='.repeat(60));

        await page.goto(pageInfo.url, {
            waitUntil: 'networkidle2',
            timeout: 10000
        });

        // Wait a bit for Streamlit to render
        await new Promise(resolve => setTimeout(resolve, 3000));

        // Check for error messages in the DOM
        const errorElements = await page.$$eval('[data-testid="stException"], .stException, [class*="error"]',
            elements => elements.map(el => el.textContent)
        );

        if (errorElements.length > 0) {
            console.log('\n❌ DOM Errors found:');
            errorElements.forEach(err => console.log(`  - ${err}`));
        }

        if (errors.length > 0) {
            console.log('\n❌ Console Errors:');
            errors.forEach(err => console.log(`  - ${err}`));
        }

        if (consoleMessages.length > 0) {
            console.log('\n📝 Console Messages:');
            consoleMessages.forEach(msg => {
                if (msg.type === 'error') {
                    console.log(`  [ERROR] ${msg.text}`);
                } else if (msg.type === 'warning') {
                    console.log(`  [WARN] ${msg.text}`);
                }
            });
        }

        if (errors.length === 0 && errorElements.length === 0) {
            console.log('\n✅ No errors found');
        }

        // Take a screenshot
        const filename = `screenshot_${pageInfo.name.replace(/[^a-zA-Z0-9]/g, '_')}.png`;
        await page.screenshot({ path: filename, fullPage: true });
        console.log(`📸 Screenshot saved: ${filename}`);

    } catch (error) {
        console.log(`\n❌ Failed to load page: ${error.message}`);
    }
}

async function main() {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    for (const pageInfo of pages) {
        await checkPage(page, pageInfo);
    }

    await browser.close();
    console.log('\n' + '='.repeat(60));
    console.log('All pages checked');
    console.log('='.repeat(60));
}

main().catch(console.error);
