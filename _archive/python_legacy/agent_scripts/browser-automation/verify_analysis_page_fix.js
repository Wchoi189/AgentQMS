const puppeteer = require('puppeteer');

async function verifyAnalysisPageFix() {
    console.log('\n' + '='.repeat(70));
    console.log('VERIFYING: Analysis Page Fixes');
    console.log('='.repeat(70));
    console.log('Checking for:');
    console.log('  1. Nested component rendering fix (_process_component error)');
    console.log('  2. PyArrow serialization fix (mixed types in Value column)');
    console.log('  3. Data loading after experiment selection');
    console.log('='.repeat(70));

    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();

        // Capture console errors
        const consoleErrors = [];
        const pageErrors = [];
        const consoleMessages = [];

        page.on('console', msg => {
            const text = msg.text();
            const type = msg.type();
            consoleMessages.push({ type, text });
            if (type === 'error') {
                consoleErrors.push(text);
            }
        });

        page.on('pageerror', error => {
            pageErrors.push(error.message);
        });

        // Navigate to Analysis page
        const url = 'http://localhost:8501/Advanced_Analysis';
        console.log(`\n📍 Navigating to: ${url}`);

        await page.goto(url, {
            waitUntil: 'networkidle2',
            timeout: 30000
        });

        // Wait for Streamlit app to initialize
        console.log('⏳ Waiting for Streamlit to initialize...');
        try {
            await page.waitForSelector('[data-testid="stAppViewContainer"]', { timeout: 10000 });
            console.log('  ✅ Streamlit container found');
        } catch (e) {
            console.log('  ⚠️  Streamlit container not found, continuing...');
        }

        // Wait for page content
        await new Promise(resolve => setTimeout(resolve, 5000));

        // Check for experiment selector
        console.log('\n🔍 Checking for experiment selector...');
        const hasExperimentSelector = await page.evaluate(() => {
            const bodyText = document.body.innerText;
            return bodyText.includes('Experiment') || bodyText.includes('Select an experiment');
        });
        console.log(`  ${hasExperimentSelector ? '✅' : '⚠️'} Experiment selector found: ${hasExperimentSelector}`);

        // Try to select an experiment if available
        console.log('\n🔍 Attempting to interact with experiment selector...');
        try {
            // Look for selectbox or similar element
            const selectboxExists = await page.evaluate(() => {
                const selectboxes = document.querySelectorAll('[data-baseweb="select"]');
                return selectboxes.length > 0;
            });

            if (selectboxExists) {
                console.log('  ✅ Found selectbox, attempting selection...');

                // Click on the selectbox
                await page.click('[data-baseweb="select"]').catch(() => {});
                await new Promise(resolve => setTimeout(resolve, 1000));

                // Try to select first option
                const options = await page.$$('[role="option"]');
                if (options.length > 0) {
                    await options[0].click().catch(() => {});
                    console.log('  ✅ Selected an experiment');

                    // Wait for data to load
                    await new Promise(resolve => setTimeout(resolve, 5000));
                }
            }
        } catch (e) {
            console.log(`  ⚠️  Could not interact with selector: ${e.message}`);
        }

        // Get page content
        const bodyText = await page.evaluate(() => document.body.innerText);

        // Check for fixed errors
        console.log('\n📊 Checking for Fixed Errors:');
        console.log('─'.repeat(70));

        // 1. Check for _process_component error (should NOT exist)
        const processComponentError = bodyText.includes('_process_component') ||
                                     consoleErrors.some(e => e.includes('_process_component')) ||
                                     pageErrors.some(e => e.includes('_process_component'));
        console.log(`  1. _process_component error: ${processComponentError ? '❌ STILL EXISTS' : '✅ FIXED'}`);
        if (processComponentError) {
            console.log('     This error should be fixed!');
        }

        // 2. Check for PyArrow serialization error (should NOT exist)
        const pyarrowError = bodyText.includes('cannot mix list and non-list') ||
                           bodyText.includes('ArrowInvalid') ||
                           consoleErrors.some(e => e.includes('cannot mix list')) ||
                           pageErrors.some(e => e.includes('ArrowInvalid'));
        console.log(`  2. PyArrow serialization error: ${pyarrowError ? '❌ STILL EXISTS' : '✅ FIXED'}`);
        if (pyarrowError) {
            console.log('     This error should be fixed!');
        }

        // 3. Check for nested component errors (should NOT exist)
        const nestedComponentError = consoleErrors.some(e =>
            e.includes('nested components') && e.includes('AttributeError')
        ) || pageErrors.some(e => e.includes('nested components'));
        console.log(`  3. Nested component rendering error: ${nestedComponentError ? '❌ STILL EXISTS' : '✅ FIXED'}`);
        if (nestedComponentError) {
            console.log('     Nested components should render properly now!');
        }

        // 4. Check for performance metrics table
        const hasMetricsTable = bodyText.includes('Performance Metrics') ||
                               bodyText.includes('Success Rate') ||
                               bodyText.includes('Total Tokens');
        console.log(`  4. Performance metrics table visible: ${hasMetricsTable ? '✅ YES' : '⚠️  NOT FOUND'}`);

        // 5. Check for expander sections
        const hasExpanders = await page.evaluate(() => {
            const expanders = document.querySelectorAll('[data-testid="stExpander"]');
            return expanders.length > 0;
        });
        console.log(`  5. Expander sections found: ${hasExpanders ? `✅ YES (${await page.evaluate(() => document.querySelectorAll('[data-testid="stExpander"]').length)} expanders)` : '⚠️  NOT FOUND'}`);

        // Summary
        console.log('\n' + '='.repeat(70));
        console.log('SUMMARY:');
        console.log('='.repeat(70));

        const allFixed = !processComponentError && !pyarrowError && !nestedComponentError;

        if (allFixed) {
            console.log('✅ All critical errors are FIXED!');
        } else {
            console.log('❌ Some errors still exist. Check details above.');
        }

        // Report console errors
        if (consoleErrors.length > 0) {
            console.log(`\n⚠️  Console Errors Found (${consoleErrors.length}):`);
            consoleErrors.slice(0, 5).forEach((error, i) => {
                console.log(`  ${i + 1}. ${error.substring(0, 100)}`);
            });
            if (consoleErrors.length > 5) {
                console.log(`  ... and ${consoleErrors.length - 5} more`);
            }
        }

        // Report page errors
        if (pageErrors.length > 0) {
            console.log(`\n❌ Page Errors Found (${pageErrors.length}):`);
            pageErrors.forEach((error, i) => {
                console.log(`  ${i + 1}. ${error}`);
            });
        }

        // Check for warnings about missing processor
        const missingProcessorWarnings = consoleMessages.filter(m =>
            m.text.includes('No processor available') ||
            m.text.includes('processor')
        );
        if (missingProcessorWarnings.length > 0) {
            console.log(`\n⚠️  Processor-related messages (${missingProcessorWarnings.length}):`);
            missingProcessorWarnings.slice(0, 3).forEach((msg, i) => {
                console.log(`  ${i + 1}. [${msg.type}] ${msg.text.substring(0, 80)}`);
            });
        }

        console.log('\n' + '='.repeat(70));

        return {
            success: allFixed,
            processComponentError,
            pyarrowError,
            nestedComponentError,
            hasMetricsTable,
            hasExpanders,
            consoleErrors: consoleErrors.length,
            pageErrors: pageErrors.length
        };

    } catch (error) {
        console.error('\n❌ Error during verification:', error);
        return {
            success: false,
            error: error.message
        };
    } finally {
        await browser.close();
    }
}

// Run the verification
if (require.main === module) {
    verifyAnalysisPageFix()
        .then(result => {
            process.exit(result.success ? 0 : 1);
        })
        .catch(error => {
            console.error('Fatal error:', error);
            process.exit(1);
        });
}

module.exports = { verifyAnalysisPageFix };

