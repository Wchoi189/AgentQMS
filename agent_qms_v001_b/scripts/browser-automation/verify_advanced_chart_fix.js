const puppeteer = require('puppeteer');

async function verifyAdvancedChartFix() {
    console.log('\n' + '='.repeat(70));
    console.log('VERIFYING: advanced_chart Component Fix');
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

        page.on('console', msg => {
            if (msg.type() === 'error') {
                consoleErrors.push(msg.text());
            }
        });

        page.on('pageerror', error => {
            pageErrors.push(error.message);
        });

        // Use correct URL format (without page number prefix)
        const url = 'http://localhost:8501/Advanced_Analysis';
        console.log(`\n📍 Navigating to: ${url}`);

        await page.goto(url, {
            waitUntil: 'networkidle2',
            timeout: 30000
        });

        // Wait for Streamlit app to fully initialize
        console.log('⏳ Waiting for Streamlit to initialize...');

        // Wait for Streamlit's main container
        try {
            await page.waitForSelector('[data-testid="stAppViewContainer"]', { timeout: 10000 });
            console.log('  ✅ Streamlit container found');
        } catch (e) {
            console.log('  ⚠️  Streamlit container not found, continuing...');
        }

        // Wait for any initial content to render
        await new Promise(resolve => setTimeout(resolve, 3000));

        // Check if page has loaded by looking for any text content
        const hasContent = await page.evaluate(() => {
            const bodyText = document.body.innerText || '';
            return bodyText.length > 100; // Should have substantial content
        });

        if (!hasContent) {
            console.log('  ⚠️  Page content seems empty, waiting longer...');
            await new Promise(resolve => setTimeout(resolve, 5000));
        }

        console.log('  ✅ Initial render complete');

        // Try to select an experiment if on Analysis/Advanced Analysis page
        try {
            console.log('🔍 Looking for experiment selector...');

            // Wait for selectbox to appear
            await page.waitForSelector('[data-testid="stSelectbox"]', { timeout: 5000 }).catch(() => null);

            const selectboxes = await page.$$('[data-testid="stSelectbox"]');
            console.log(`  Found ${selectboxes.length} selectbox(es)`);

            // Try to interact with the first selectbox (usually experiment selector)
            if (selectboxes.length > 0) {
                console.log('  📝 Attempting to select an experiment...');

                // Use Puppeteer's keyboard navigation to select an option
                await selectboxes[0].click();
                await new Promise(resolve => setTimeout(resolve, 500));

                // Try arrow key navigation
                await page.keyboard.press('ArrowDown');
                await new Promise(resolve => setTimeout(resolve, 300));
                await page.keyboard.press('Enter');

                console.log('  ⏳ Waiting for page to re-render after selection...');
                await new Promise(resolve => setTimeout(resolve, 5000));

                // Wait for Streamlit to finish rerunning
                await page.waitForFunction(
                    () => !document.querySelector('[data-testid="stAppViewContainer"]')?.classList.contains('stAppViewContainer') ||
                        document.querySelector('[data-testid="stAppViewContainer"]')?.getAttribute('data-state') === 'ready',
                    { timeout: 10000 }
                ).catch(() => {
                    console.log('  ℹ️  Could not detect rerun completion, continuing anyway...');
                });

                await new Promise(resolve => setTimeout(resolve, 2000));
                console.log('  ✅ Selection complete');
            }
        } catch (e) {
            console.log(`  ℹ️  Could not interact with experiment selector: ${e.message}`);
        }

        // Get page content
        const bodyText = await page.evaluate(() => document.body.innerText);

        // DEBUG: Output page content analysis (can be removed later if not needed)
        // console.log('\n📄 DEBUG: Page content analysis:');
        // console.log(`  Total text length: ${bodyText.length} characters`);
        // console.log(`  Contains "Select": ${bodyText.includes('Select')}`);
        // console.log(`  Contains "experiment": ${bodyText.toLowerCase().includes('experiment')}`);
        // console.log(`  Contains "Analysis": ${bodyText.includes('Analysis')}`);
        // console.log('');

        // Check for the specific error we fixed
        const fixedErrorPatterns = [
            'Unsupported custom component type: advanced_chart',
            'ValueError.*advanced_chart',
            'No renderer registered for component type: advanced_chart'
        ];

        console.log('\n🔍 Checking for fixed errors...');
        let foundErrors = false;
        for (const pattern of fixedErrorPatterns) {
            const regex = new RegExp(pattern, 'i');
            if (regex.test(bodyText)) {
                console.log(`  ❌ FOUND FIXED ERROR: ${pattern}`);
                foundErrors = true;
                // Show context
                const index = bodyText.search(regex);
                const context = bodyText.substring(Math.max(0, index - 100), Math.min(bodyText.length, index + 200));
                console.log(`     Context: ${context.replace(/\n/g, ' ')}`);
            }
        }

        if (!foundErrors) {
            console.log('  ✅ No advanced_chart rendering errors found!');
        }

        // Check for user-visible error/warning messages
        console.log('\n🔍 Checking for user-visible error messages...');
        const userVisibleErrors = [];

        // Expander validation errors
        const expanderErrors = (bodyText.match(/⚠️ Error in validating expander config/g) || []).length;
        if (expanderErrors > 0) {
            userVisibleErrors.push({
                type: 'Expander Validation Error',
                count: expanderErrors,
                pattern: '⚠️ Error in validating expander config'
            });
        }

        // "No data available" messages
        const noDataMessages = (bodyText.match(/No data available for [^\n]+/g) || []).length;
        if (noDataMessages > 0) {
            userVisibleErrors.push({
                type: 'No Data Available',
                count: noDataMessages,
                pattern: 'No data available for'
            });
        }

        // ExperimentResult validation errors
        const experimentErrors = (bodyText.match(/Failed to load new format experiment|validation error for ExperimentResult|Field required.*metadata/g) || []).length;
        if (experimentErrors > 0) {
            userVisibleErrors.push({
                type: 'ExperimentResult Validation Error',
                count: experimentErrors,
                pattern: 'ExperimentResult.*metadata.*Field required'
            });
        }

        // Check Streamlit warning/error elements in DOM
        const streamlitErrors = await page.evaluate(() => {
            // Look for Streamlit error/warning elements - comprehensive selectors
            // Includes Streamlit-specific selectors: div[data-testid="st alert"] and variations
            const allPossibleElements = Array.from(document.querySelectorAll(
                '[data-testid="stException"], ' +
                '[data-testid="st alert"], ' +
                '[data-testid="stAlert"], ' +
                '.stException, ' +
                '[data-testid*="error"], ' +
                '[data-testid*="warning"], ' +
                '[data-testid*="alert"], ' +
                '[class*="stAlert"], ' +
                '[class*="st-emotion-cache"], ' +
                '[data-baseweb="notification"], ' +
                '[role="alert"], ' +
                '.alert, ' +
                '[class*="alert"]'
            ));

            const errors = [];

            // Also search by text content for warnings/errors
            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_TEXT,
                null
            );

            let node;
            const errorTexts = new Set();
            while (node = walker.nextNode()) {
                const text = node.textContent || '';
                // Check for error patterns in any text node
                if (text.includes('⚠️') ||
                    text.includes('Error in validating') ||
                    text.includes('Invalid expander') ||
                    text.includes('No data available') ||
                    text.includes('Field required') ||
                    text.includes('validation error')) {
                    // Get parent element that contains this text
                    let parent = node.parentElement;
                    while (parent && parent !== document.body) {
                        const parentText = parent.innerText || parent.textContent || '';
                        if (parentText.trim().length > 0 && parentText.length < 500) {
                            errorTexts.add(parentText.trim());
                            break;
                        }
                        parent = parent.parentElement;
                    }
                }
            }

            // Convert set to array
            Array.from(errorTexts).forEach(text => errors.push(text));

            // Also check the structured elements
            allPossibleElements.forEach(el => {
                const text = el.innerText || el.textContent || '';
                if (text.trim().length > 0 && text.length < 1000) {
                    const isError = text.includes('⚠️') ||
                        text.includes('Error') ||
                        text.includes('error') ||
                        text.includes('❌') ||
                        text.includes('Warning') ||
                        text.includes('warning') ||
                        text.includes('Invalid') ||
                        text.includes('validation');

                    if (isError) {
                        errors.push(text.trim());
                    }
                }
            });

            // Remove duplicates
            return [...new Set(errors)];
        });

        // Report findings
        if (userVisibleErrors.length > 0 || streamlitErrors.length > 0) {
            console.log('  ⚠️  Found user-visible errors/warnings:');
            userVisibleErrors.forEach(err => {
                console.log(`     - ${err.type}: ${err.count} occurrence(s)`);
            });
            if (streamlitErrors.length > 0) {
                console.log(`     - Streamlit DOM errors: ${streamlitErrors.length} element(s)`);
                streamlitErrors.slice(0, 5).forEach((err, idx) => {
                    console.log(`       ${idx + 1}. ${err.substring(0, 150)}${err.length > 150 ? '...' : ''}`);
                });
            }
        } else {
            console.log('  ✅ No user-visible error messages found!');
        }

        // Check for visualizations (chart elements)
        console.log('\n📊 Checking for visualization components...');
        const chartElements = await page.evaluate(() => {
            // Look for common chart container elements
            const possibleSelectors = [
                '[data-testid*="chart"]',
                '[class*="chart"]',
                'canvas',
                'svg',
                '[class*="plot"]',
                '[class*="graph"]'
            ];

            let count = 0;
            for (const selector of possibleSelectors) {
                try {
                    const elements = document.querySelectorAll(selector);
                    count += elements.length;
                } catch (e) {
                    // Selector might be invalid, skip
                }
            }
            return count;
        });

        console.log(`  Found ${chartElements} potential chart/visualization elements`);

        // Check for Streamlit exception elements
        const exceptionElements = await page.evaluate(() => {
            const exceptions = document.querySelectorAll('[data-testid="stException"], .stException');
            return Array.from(exceptions).map(el => el.innerText).filter(text => text.length > 0);
        });

        if (exceptionElements.length > 0) {
            console.log(`\n⚠️  Found ${exceptionElements.length} Streamlit exception(s):`);
            exceptionElements.forEach((error, idx) => {
                console.log(`  ${idx + 1}. ${error.substring(0, 200)}...`);
            });
        } else {
            console.log('\n✅ No Streamlit exceptions visible on page!');
        }

        // Report console and page errors (filter out non-critical 404s)
        const criticalErrors = consoleErrors.filter(err =>
            !err.includes('404') &&
            !err.includes('favicon') &&
            !err.toLowerCase().includes('not found')
        );
        const criticalPageErrors = pageErrors.filter(err =>
            !err.includes('404') &&
            !err.includes('favicon')
        );

        console.log('\n🔍 Browser Console Errors:');
        if (criticalErrors.length === 0 && criticalPageErrors.length === 0) {
            console.log('  ✅ No critical JavaScript errors found!');
            if (consoleErrors.length > 0 || pageErrors.length > 0) {
                console.log(`  ℹ️  (Ignored ${consoleErrors.length + pageErrors.length - criticalErrors.length - criticalPageErrors.length} non-critical 404/favicon errors)`);
            }
        } else {
            criticalErrors.forEach(err => console.log(`  ⚠️  Console: ${err}`));
            criticalPageErrors.forEach(err => console.log(`  ⚠️  Page: ${err}`));
        }

        // Summary
        console.log('\n' + '='.repeat(70));
        console.log('SUMMARY');
        console.log('='.repeat(70));
        const hasFixedError = foundErrors;
        const hasExceptions = exceptionElements.length > 0;
        const hasUserVisibleErrors = userVisibleErrors.length > 0 || streamlitErrors.length > 0;
        const criticalJsErrors = consoleErrors.filter(err =>
            !err.includes('404') &&
            !err.includes('favicon') &&
            !err.toLowerCase().includes('not found')
        );
        const criticalPageErrs = pageErrors.filter(err =>
            !err.includes('404') &&
            !err.includes('favicon')
        );
        const hasJsErrors = criticalJsErrors.length > 0 || criticalPageErrs.length > 0;

        if (!hasFixedError && !hasExceptions && !hasJsErrors && !hasUserVisibleErrors) {
            console.log('✅ VERIFICATION PASSED: advanced_chart fix is working!');
            console.log(`   - No rendering errors found`);
            console.log(`   - No Streamlit exceptions`);
            console.log(`   - No JavaScript errors`);
            console.log(`   - No user-visible error messages`);
            console.log(`   - ${chartElements} visualization elements detected`);
        } else {
            console.log('⚠️  ISSUES FOUND:');
            if (hasFixedError) console.log('   - Fixed errors still appearing');
            if (hasExceptions) console.log(`   - ${exceptionElements.length} Streamlit exception(s)`);
            if (hasJsErrors) console.log('   - JavaScript errors in console');
            if (hasUserVisibleErrors) {
                console.log('   - User-visible errors/warnings:');
                userVisibleErrors.forEach(err => console.log(`     • ${err.type}: ${err.count}`));
                if (streamlitErrors.length > 0) console.log(`     • Streamlit DOM errors: ${streamlitErrors.length}`);
            }
        }
        console.log('='.repeat(70) + '\n');

        return {
            success: !hasFixedError && !hasExceptions && !hasJsErrors && !hasUserVisibleErrors,
            fixedErrorFound: hasFixedError,
            exceptions: exceptionElements.length,
            jsErrors: criticalJsErrors.length + criticalPageErrs.length,
            userVisibleErrors: userVisibleErrors.length,
            streamlitErrors: streamlitErrors.length,
            chartElements: chartElements,
            errorDetails: {
                expanderErrors: userVisibleErrors.find(e => e.type === 'Expander Validation Error')?.count || 0,
                noDataMessages: userVisibleErrors.find(e => e.type === 'No Data Available')?.count || 0,
                experimentErrors: userVisibleErrors.find(e => e.type === 'ExperimentResult Validation Error')?.count || 0
            }
        };

    } finally {
        await browser.close();
    }
}

async function verifyEnhancedDataTable() {
    console.log('\n' + '='.repeat(70));
    console.log('VERIFYING: Enhanced Data Table Fix');
    console.log('='.repeat(70));

    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();

        const consoleErrors = [];
        const pageErrors = [];

        page.on('console', msg => {
            if (msg.type() === 'error') {
                consoleErrors.push(msg.text());
            }
        });

        page.on('pageerror', error => {
            pageErrors.push(error.message);
        });

        const url = 'http://localhost:8501/Data_Explorer';
        console.log(`\n📍 Navigating to: ${url}`);

        await page.goto(url, {
            waitUntil: 'networkidle2',
            timeout: 30000
        });

        console.log('⏳ Waiting for page to fully render...');
        await new Promise(resolve => setTimeout(resolve, 5000));

        const bodyText = await page.evaluate(() => document.body.innerText);

        // Check for enhanced table features (color coding, two-row format indicators)
        console.log('\n🔍 Checking for enhanced data table features...');

        // Look for table elements
        const tableInfo = await page.evaluate(() => {
            const tables = document.querySelectorAll('table, [data-testid*="table"], [class*="table"]');
            return {
                count: tables.length,
                hasStyledRows: false,
                hasColorCoding: false
            };
        });

        console.log(`  Found ${tableInfo.count} table element(s)`);

        // Check for enhanced table specific features
        const hasEnhancedFeatures = bodyText.includes('Error Data Table') ||
            bodyText.includes('Two-row format') ||
            bodyText.includes('color-coded');

        // Check for removed elements (old view selectors should NOT be present)
        const hasOldSelectors = bodyText.includes('Table View Mode') ||
            bodyText.includes('Standard View') ||
            bodyText.includes('Enhanced View') ||
            bodyText.includes('Diff Mode Preference');

        console.log('\n🔍 Checking for obsolete UI elements...');
        if (hasOldSelectors) {
            console.log('  ⚠️  Found obsolete view selectors (should be removed)');
        } else {
            console.log('  ✅ Old view selectors correctly removed');
        }

        // Check for user-visible error/warning messages on Data Explorer
        console.log('\n🔍 Checking for user-visible error messages...');
        const userVisibleErrors = [];

        // Expander validation errors
        const expanderErrors = (bodyText.match(/⚠️ Error in validating expander config/g) || []).length;
        if (expanderErrors > 0) {
            userVisibleErrors.push({
                type: 'Expander Validation Error',
                count: expanderErrors,
                pattern: '⚠️ Error in validating expander config'
            });
        }

        // "No data available" messages
        const noDataMessages = (bodyText.match(/No data available for [^\n]+/g) || []).length;
        if (noDataMessages > 0) {
            userVisibleErrors.push({
                type: 'No Data Available',
                count: noDataMessages,
                pattern: 'No data available for'
            });
        }

        // Check Streamlit warning/error elements in DOM
        const streamlitErrors = await page.evaluate(() => {
            // Comprehensive search for error/warning text in DOM
            // Includes Streamlit-specific selectors: div[data-testid="st alert"] and variations
            const allPossibleElements = Array.from(document.querySelectorAll(
                '[data-testid="stException"], ' +
                '[data-testid="st alert"], ' +
                '[data-testid="stAlert"], ' +
                '.stException, ' +
                '[data-testid*="error"], ' +
                '[data-testid*="warning"], ' +
                '[data-testid*="alert"], ' +
                '[class*="stAlert"], ' +
                '[class*="st-emotion-cache"], ' +
                '[data-baseweb="notification"], ' +
                '[role="alert"], ' +
                '.alert, ' +
                '[class*="alert"]'
            ));

            const errors = [];

            // Search by text content using TreeWalker
            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_TEXT,
                null
            );

            let node;
            const errorTexts = new Set();
            while (node = walker.nextNode()) {
                const text = node.textContent || '';
                if (text.includes('⚠️') ||
                    text.includes('Error in validating') ||
                    text.includes('Invalid expander') ||
                    text.includes('No data available') ||
                    text.includes('Field required')) {
                    let parent = node.parentElement;
                    while (parent && parent !== document.body) {
                        const parentText = parent.innerText || parent.textContent || '';
                        if (parentText.trim().length > 0 && parentText.length < 500) {
                            errorTexts.add(parentText.trim());
                            break;
                        }
                        parent = parent.parentElement;
                    }
                }
            }

            Array.from(errorTexts).forEach(text => errors.push(text));

            // Check structured elements
            allPossibleElements.forEach(el => {
                const text = el.innerText || el.textContent || '';
                if (text.trim().length > 0 && text.length < 1000) {
                    const isError = text.includes('⚠️') ||
                        text.includes('Error') ||
                        text.includes('Invalid') ||
                        text.includes('validation') ||
                        text.includes('Warning');

                    if (isError) {
                        errors.push(text.trim());
                    }
                }
            });

            return [...new Set(errors)];
        });

        // Report findings
        if (userVisibleErrors.length > 0 || streamlitErrors.length > 0) {
            console.log('  ⚠️  Found user-visible errors/warnings:');
            userVisibleErrors.forEach(err => {
                console.log(`     - ${err.type}: ${err.count} occurrence(s)`);
            });
            if (streamlitErrors.length > 0) {
                console.log(`     - Streamlit DOM errors: ${streamlitErrors.length} element(s)`);
                streamlitErrors.slice(0, 5).forEach((err, idx) => {
                    console.log(`       ${idx + 1}. ${err.substring(0, 150)}${err.length > 150 ? '...' : ''}`);
                });
            }
        } else {
            console.log('  ✅ No user-visible error messages found!');
        }

        // Check for Streamlit exceptions
        const exceptionElements = await page.evaluate(() => {
            const exceptions = document.querySelectorAll('[data-testid="stException"], .stException');
            return Array.from(exceptions).map(el => el.innerText).filter(text => text.length > 0);
        });

        if (exceptionElements.length > 0) {
            console.log(`\n⚠️  Found ${exceptionElements.length} Streamlit exception(s):`);
            exceptionElements.forEach((error, idx) => {
                console.log(`  ${idx + 1}. ${error.substring(0, 200)}...`);
            });
        } else {
            console.log('\n✅ No Streamlit exceptions visible on page!');
        }

        // Filter out non-critical 404s
        const criticalErrors = consoleErrors.filter(err =>
            !err.includes('404') &&
            !err.includes('favicon') &&
            !err.toLowerCase().includes('not found')
        );
        const criticalPageErrors = pageErrors.filter(err =>
            !err.includes('404') &&
            !err.includes('favicon')
        );

        console.log('\n🔍 Browser Console Errors:');
        if (criticalErrors.length === 0 && criticalPageErrors.length === 0) {
            console.log('  ✅ No critical JavaScript errors found!');
            if (consoleErrors.length > 0 || pageErrors.length > 0) {
                console.log(`  ℹ️  (Ignored ${consoleErrors.length + pageErrors.length - criticalErrors.length - criticalPageErrors.length} non-critical 404/favicon errors)`);
            }
        } else {
            criticalErrors.forEach(err => console.log(`  ⚠️  Console: ${err}`));
            criticalPageErrors.forEach(err => console.log(`  ⚠️  Page: ${err}`));
        }

        // Summary
        console.log('\n' + '='.repeat(70));
        console.log('SUMMARY');
        console.log('='.repeat(70));
        const hasExceptions = exceptionElements.length > 0;
        const hasUserVisibleErrors = userVisibleErrors.length > 0 || streamlitErrors.length > 0;
        const criticalJsErrors = consoleErrors.filter(err =>
            !err.includes('404') &&
            !err.includes('favicon') &&
            !err.toLowerCase().includes('not found')
        );
        const criticalPageErrs = pageErrors.filter(err =>
            !err.includes('404') &&
            !err.includes('favicon')
        );
        const hasJsErrors = criticalJsErrors.length > 0 || criticalPageErrs.length > 0;
        const hasObsoleteUI = hasOldSelectors;

        if (!hasExceptions && !hasJsErrors && !hasObsoleteUI && !hasUserVisibleErrors) {
            console.log('✅ VERIFICATION PASSED: Enhanced data table fix is working!');
            console.log(`   - No Streamlit exceptions`);
            console.log(`   - No JavaScript errors`);
            console.log(`   - Obsolete UI elements removed`);
            console.log(`   - No user-visible error messages`);
            console.log(`   - ${tableInfo.count} table element(s) found`);
        } else {
            console.log('⚠️  ISSUES FOUND:');
            if (hasExceptions) console.log(`   - ${exceptionElements.length} Streamlit exception(s)`);
            if (hasJsErrors) console.log('   - JavaScript errors in console');
            if (hasObsoleteUI) console.log('   - Obsolete UI elements still present');
            if (hasUserVisibleErrors) {
                console.log('   - User-visible errors/warnings:');
                userVisibleErrors.forEach(err => console.log(`     • ${err.type}: ${err.count}`));
                if (streamlitErrors.length > 0) console.log(`     • Streamlit DOM errors: ${streamlitErrors.length}`);
            }
        }
        console.log('='.repeat(70) + '\n');

        return {
            success: !hasExceptions && !hasJsErrors && !hasObsoleteUI && !hasUserVisibleErrors,
            exceptions: exceptionElements.length,
            jsErrors: criticalJsErrors.length + criticalPageErrs.length,
            obsoleteUI: hasObsoleteUI,
            userVisibleErrors: userVisibleErrors.length,
            streamlitErrors: streamlitErrors.length,
            tableElements: tableInfo.count,
            errorDetails: {
                expanderErrors: userVisibleErrors.find(e => e.type === 'Expander Validation Error')?.count || 0,
                noDataMessages: userVisibleErrors.find(e => e.type === 'No Data Available')?.count || 0
            }
        };

    } finally {
        await browser.close();
    }
}

(async () => {
    console.log('\n🔍 COMPREHENSIVE FIX VERIFICATION');
    console.log('Testing advanced_chart and enhanced_data_table fixes\n');

    const results = {
        advancedChart: await verifyAdvancedChartFix(),
        enhancedDataTable: await verifyEnhancedDataTable()
    };

    // Final summary
    console.log('\n' + '='.repeat(70));
    console.log('FINAL VERIFICATION SUMMARY');
    console.log('='.repeat(70));
    console.log(`\nAdvanced Chart Fix: ${results.advancedChart.success ? '✅ PASSED' : '❌ FAILED'}`);
    if (!results.advancedChart.success) {
        if (results.advancedChart.fixedErrorFound) console.log('   - Fixed error still appearing');
        if (results.advancedChart.exceptions > 0) console.log(`   - ${results.advancedChart.exceptions} exception(s)`);
        if (results.advancedChart.jsErrors > 0) console.log(`   - ${results.advancedChart.jsErrors} JS error(s)`);
        if (results.advancedChart.userVisibleErrors > 0 || results.advancedChart.streamlitErrors > 0) {
            console.log(`   - User-visible errors: ${results.advancedChart.userVisibleErrors + results.advancedChart.streamlitErrors}`);
            if (results.advancedChart.errorDetails) {
                if (results.advancedChart.errorDetails.expanderErrors > 0) {
                    console.log(`     • Expander validation: ${results.advancedChart.errorDetails.expanderErrors}`);
                }
                if (results.advancedChart.errorDetails.noDataMessages > 0) {
                    console.log(`     • No data messages: ${results.advancedChart.errorDetails.noDataMessages}`);
                }
                if (results.advancedChart.errorDetails.experimentErrors > 0) {
                    console.log(`     • ExperimentResult validation: ${results.advancedChart.errorDetails.experimentErrors}`);
                }
            }
        }
    } else {
        console.log(`   - ${results.advancedChart.chartElements} visualization elements found`);
    }

    console.log(`\nEnhanced Data Table Fix: ${results.enhancedDataTable.success ? '✅ PASSED' : '❌ FAILED'}`);
    if (!results.enhancedDataTable.success) {
        if (results.enhancedDataTable.exceptions > 0) console.log(`   - ${results.enhancedDataTable.exceptions} exception(s)`);
        if (results.enhancedDataTable.jsErrors > 0) console.log(`   - ${results.enhancedDataTable.jsErrors} JS error(s)`);
        if (results.enhancedDataTable.obsoleteUI) console.log('   - Obsolete UI elements present');
        if (results.enhancedDataTable.userVisibleErrors > 0 || results.enhancedDataTable.streamlitErrors > 0) {
            console.log(`   - User-visible errors: ${results.enhancedDataTable.userVisibleErrors + results.enhancedDataTable.streamlitErrors}`);
            if (results.enhancedDataTable.errorDetails) {
                if (results.enhancedDataTable.errorDetails.expanderErrors > 0) {
                    console.log(`     • Expander validation: ${results.enhancedDataTable.errorDetails.expanderErrors}`);
                }
                if (results.enhancedDataTable.errorDetails.noDataMessages > 0) {
                    console.log(`     • No data messages: ${results.enhancedDataTable.errorDetails.noDataMessages}`);
                }
            }
        }
    } else {
        console.log(`   - ${results.enhancedDataTable.tableElements} table element(s) found`);
    }

    const allPassed = results.advancedChart.success && results.enhancedDataTable.success;
    console.log('\n' + '='.repeat(70));
    if (allPassed) {
        console.log('✅ ALL FIXES VERIFIED SUCCESSFULLY!');
    } else {
        console.log('⚠️  SOME ISSUES FOUND - REVIEW NEEDED');
    }
    console.log('='.repeat(70) + '\n');

    process.exit(allPassed ? 0 : 1);
})();

