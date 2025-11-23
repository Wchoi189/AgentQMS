const puppeteer = require('puppeteer');

async function detailedTest(url) {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push('Console: ' + msg.text());
  });

  page.on('pageerror', err => errors.push('Page: ' + err.message));

  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 3000));

  const bodyText = await page.evaluate(() => document.body.innerText);

  const checks = {
    hasTitle: await page.title(),
    selectboxes: (await page.$$('[data-testid="stSelectbox"]')).length,
    buttons: (await page.$$('button')).length,
    inputs: (await page.$$('input, textarea')).length,
    hasErrors: bodyText.includes('Traceback') || bodyText.includes('AttributeError'),
    loaderFixed: !bodyText.includes('get_about_content'),
    validationFixed: !bodyText.includes('Invalid prompt type'),
    componentFixed: !bodyText.includes('component.props'),
    radioFixed: !bodyText.includes('single is not in iterable')
  };

  await browser.close();

  return { checks, errors, bodyText: bodyText.substring(0, 500) };
}

(async () => {
  console.log('Comprehensive Streamlit Test\n');
  const result = await detailedTest('http://localhost:8501/');

  console.log('Page Info:');
  console.log('  Title: ' + result.checks.hasTitle);
  console.log('  UI Elements: ' + (result.checks.selectboxes + result.checks.buttons + result.checks.inputs));

  console.log('\nFix Verification:');
  console.log('  Loader functions: ' + (result.checks.loaderFixed ? '✅' : '❌'));
  console.log('  Validation errors: ' + (result.checks.validationFixed ? '✅' : '❌'));
  console.log('  Component attrs: ' + (result.checks.componentFixed ? '✅' : '❌'));
  console.log('  Radio state: ' + (result.checks.radioFixed ? '✅' : '❌'));
  console.log('  No Python errors: ' + (!result.checks.hasErrors ? '✅' : '❌'));

  console.log('\nBrowser Errors: ' + result.errors.length);
  if (result.errors.length > 0) {
    result.errors.forEach(e => console.log('  ' + e));
  }

  console.log('\nPage Preview:');
  console.log(result.bodyText.substring(0, 300));
})();
