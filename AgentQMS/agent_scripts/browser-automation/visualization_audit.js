const puppeteer = require('puppeteer');

async function auditVisualizationErrors() {
    console.log('🚀 Starting visualization audit with Puppeteer...');

    const browser = await puppeteer.launch({
        headless: true, // Run headless in server environment
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();

    // Capture console errors
    const errors = [];
    page.on('console', msg => {
        if (msg.type() === 'error') {
            errors.push({
                type: 'console',
                message: msg.text(),
                timestamp: new Date().toISOString()
            });
        }
    });

    // Capture page errors
    page.on('pageerror', error => {
        errors.push({
            type: 'pageerror',
            message: error.message,
            timestamp: new Date().toISOString()
        });
    });

    try {
        // Navigate to main page first
        console.log('📍 Navigating to main page...');
        await page.goto('http://localhost:8501', { waitUntil: 'networkidle2' });
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Test 1: Analysis Page - Word-Level Changes Error
        console.log('🔍 Testing Analysis Page...');
        await page.goto('http://localhost:8501/Analysis', { waitUntil: 'networkidle2' });
        await new Promise(resolve => setTimeout(resolve, 3000));

        // Look for Word-Level Changes section and try to trigger the error
        console.log('🔍 Looking for Word-Level Changes elements...');

        // Debug: Log all buttons on the page
        const allButtons = await page.$$('button');
        console.log(`📋 Found ${allButtons.length} buttons on the page:`);
        for (let i = 0; i < allButtons.length; i++) {
            const buttonText = await page.evaluate(el => el.textContent.trim(), allButtons[i]);
            if (buttonText) {
                console.log(`  Button ${i + 1}: "${buttonText}"`);
            }
        }

        // Try multiple selector strategies
        let wordLevelButton = null;
        for (const button of allButtons) {
            const buttonText = await page.evaluate(el => el.textContent.trim(), button);
            if (buttonText && buttonText.includes('Word-Level Changes')) {
                wordLevelButton = button;
                console.log('📊 Found Word-Level Changes button via text content');
                break;
            }
        }

        if (wordLevelButton) {
            console.log('📊 Clicking Word-Level Changes button...');
            await wordLevelButton.click();
            await new Promise(resolve => setTimeout(resolve, 2000));
        } else {
            console.log('⚠️ Word-Level Changes button not found');
        }

        // Test 2: Schema Advanced Analysis Page - Data Source Issues
        console.log('🔍 Testing Schema Advanced Analysis Page...');
        await page.goto('http://localhost:8501/schema_advanced_analysis', { waitUntil: 'networkidle2' });
        await new Promise(resolve => setTimeout(resolve, 3000));

        // Debug: Log page title and key elements
        const pageTitle = await page.title();
        console.log(`📄 Page title: ${pageTitle}`);

        // Check for data source related elements
        const selects = await page.$$('select');
        const inputs = await page.$$('input');
        const divs = await page.$$('div[role="combobox"], div[role="listbox"]');

        console.log(`📋 Found ${selects.length} select elements, ${inputs.length} input elements, ${divs.length} combobox/listbox elements`);

        // Check if data source dropdown exists and has options
        if (selects.length > 0) {
            for (let i = 0; i < selects.length; i++) {
                const options = await page.$$eval(`select:nth-of-type(${i + 1}) option`, opts => opts.map(opt => opt.textContent));
                console.log(`  Select ${i + 1} options:`, options);
            }
        }

        // Look for data overview metrics
        const dataOverviewText = await page.evaluate(() => {
            const text = document.body.textContent || '';
            return text.includes('Total Records') ? 'Found data overview section' : 'No data overview found';
        });
        console.log(`📊 Data overview: ${dataOverviewText}`);

        // Take screenshots for visual inspection
        await page.screenshot({ path: 'analysis_page_audit.png', fullPage: true });
        await page.goto('http://localhost:8501/schema_advanced_analysis', { waitUntil: 'networkidle2' });
        await page.screenshot({ path: 'schema_advanced_analysis_audit.png', fullPage: true });

        console.log('📸 Screenshots captured');

    } catch (error) {
        console.error('❌ Error during audit:', error);
        errors.push({
            type: 'script_error',
            message: error.message,
            timestamp: new Date().toISOString()
        });
    }

    // Output results
    console.log('\n📊 AUDIT RESULTS:');
    console.log('================');
    console.log(`Total errors captured: ${errors.length}`);

    if (errors.length > 0) {
        console.log('\n🚨 ERRORS FOUND:');
        errors.forEach((error, index) => {
            console.log(`${index + 1}. [${error.type.toUpperCase()}] ${error.timestamp}`);
            console.log(`   ${error.message}`);
            console.log('');
        });
    } else {
        console.log('✅ No JavaScript errors detected');
    }

    // Keep browser open for manual inspection
    console.log('🔍 Browser remains open for manual inspection');
    console.log('Press Ctrl+C to close browser and exit');

    // Don't close browser automatically - let user inspect manually
    // await browser.close();
}

auditVisualizationErrors().catch(console.error);