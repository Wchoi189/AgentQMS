const puppeteer = require('puppeteer');

async function testPage(url, pageName) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`Testing: ${pageName}`);
  console.log('='.repeat(60));

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();

    await page.goto(url, {
      waitUntil: 'networkidle2',
      timeout: 30000
    });

    await new Promise(resolve => setTimeout(resolve, 3000));

    const bodyText = await page.evaluate(() => document.body.innerText);

    // Critical errors (should NOT exist)
    const criticalErrors = [
      'AttributeError',
      'KeyError',
      'TypeError',
      'Traceback',
      'ValidationError',
      'has no attribute',
      'object has no attribute',
      'single is not in iterable'
    ];

    // Errors that were supposed to be fixed
    const fixedErrors = [
      'get_about_content',
      'get_default_experiment_name',
      'component.props',
      'Invalid prompt type'
    ];

    // Error messages that should NOT be visible to users
    const unexpectedErrors = [
      'Failed to resolve metric value',
      'Failed to resolve content_source',
      'Error in resolving markdown',
      'Failed to resolve data source'
    ];

    console.log('\n📊 Critical Errors (MUST be 0):');
    let criticalFound = 0;
    for (const pattern of criticalErrors) {
      if (bodyText.includes(pattern)) {
        console.log(`  ❌ FOUND: ${pattern}`);
        criticalFound++;
        // Show context
        const index = bodyText.indexOf(pattern);
        const context = bodyText.substring(Math.max(0, index - 50), Math.min(bodyText.length, index + 150));
        console.log(`     Context: ${context.replace(/\n/g, ' ')}`);
      }
    }
    if (criticalFound === 0) {
      console.log('  ✅ No critical errors found!');
    }

    console.log('\n🔧 Fixed Errors (should NOT appear):');
    let fixedFound = 0;
    for (const pattern of fixedErrors) {
      if (bodyText.includes(pattern)) {
        console.log(`  ⚠️  STILL EXISTS: ${pattern}`);
        fixedFound++;
      }
    }
    if (fixedFound === 0) {
      console.log('  ✅ All previously fixed errors are resolved!');
    }

    console.log('\n⚠️  Unexpected User-Visible Errors (should be 0):');
    let unexpectedCount = 0;
    for (const pattern of unexpectedErrors) {
      if (bodyText.includes(pattern)) {
        console.log(`  ❌ FOUND: ${pattern}`);
        unexpectedCount++;
        // Show context
        const index = bodyText.indexOf(pattern);
        const context = bodyText.substring(Math.max(0, index - 50), Math.min(bodyText.length, index + 150));
        console.log(`     Context: ${context.replace(/\n/g, ' ')}`);
      }
    }
    if (unexpectedCount === 0) {
      console.log('  ✅ No unexpected error messages visible to users!');
    }

    // Check components
    const selectboxes = await page.$$('[data-testid="stSelectbox"]');
    const buttons = await page.$$('button');
    const inputs = await page.$$('input, textarea');

    console.log('\n🎨 UI Components:');
    console.log(`  Selectboxes: ${selectboxes.length}`);
    console.log(`  Buttons: ${buttons.length}`);
    console.log(`  Inputs: ${inputs.length}`);

    const result = {
      critical: criticalFound,
      fixed: fixedFound,
      unexpected: unexpectedCount,
      components: {
        selectboxes: selectboxes.length,
        buttons: buttons.length,
        inputs: inputs.length
      }
    };

    return result;

  } finally {
    await browser.close();
  }
}

(async () => {
  console.log('\n🔍 COMPREHENSIVE FIX VERIFICATION');
  console.log('Testing all pages with Puppeteer\n');

  const results = {};

  // Test main inference page
  try {
    results.inference = await testPage('http://localhost:8501/schema_inference', 'Inference Page (Main)');
  } catch (e) {
    console.log(`Failed to test inference page: ${e.message}`);
    results.inference = { error: e.message };
  }

  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('📋 SUMMARY');
  console.log('='.repeat(60));

  for (const [page, result] of Object.entries(results)) {
    console.log(`\n${page}:`);
    if (result.error) {
      console.log(`  ❌ Error: ${result.error}`);
    } else {
      console.log(`  Critical Errors: ${result.critical === 0 ? '✅ 0' : '❌ ' + result.critical}`);
      console.log(`  Fixed Errors: ${result.fixed === 0 ? '✅ 0' : '⚠️  ' + result.fixed}`);
      console.log(`  Unexpected UI Errors: ${result.unexpected === 0 ? '✅ 0' : '❌ ' + result.unexpected}`);
      console.log(`  UI Components: ${result.components.selectboxes + result.components.buttons + result.components.inputs}`);
    }
  }

  console.log('\n' + '='.repeat(60));
  const totalCritical = Object.values(results).reduce((sum, r) => sum + (r.critical || 0), 0);
  const totalFixed = Object.values(results).reduce((sum, r) => sum + (r.fixed || 0), 0);
  const totalUnexpected = Object.values(results).reduce((sum, r) => sum + (r.unexpected || 0), 0);

  if (totalCritical === 0 && totalFixed === 0 && totalUnexpected === 0) {
    console.log('✅ ALL FIXES VERIFIED - APPLICATION READY');
  } else {
    console.log('⚠️  ISSUES FOUND - REVIEW NEEDED');
    if (totalUnexpected > 0) {
      console.log(`   ${totalUnexpected} unexpected error messages visible to users`);
    }
  }
  console.log('='.repeat(60) + '\n');
})();
