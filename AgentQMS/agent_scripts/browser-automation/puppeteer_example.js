#!/usr/bin/env node

/**
 * Simple Puppeteer Example - How to use Puppeteer in this project
 */

const puppeteer = require('puppeteer');

async function example() {
    console.log('🚀 Launching Puppeteer browser...');

    // Launch browser with options for this environment
    const browser = await puppeteer.launch({
        headless: true, // Set to false to see the browser window
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage' // Helps in containerized environments
        ]
    });

    try {
        console.log('📄 Creating new page...');
        const page = await browser.newPage();

        // Set viewport size
        await page.setViewport({ width: 1280, height: 720 });

        console.log('🌐 Navigating to a webpage...');
        await page.goto('https://example.com', {
            waitUntil: 'networkidle2',
            timeout: 30000
        });

        // Wait for content to load
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Get page title
        const title = await page.title();
        console.log(`📋 Page title: ${title}`);

        // Get some text content
        const heading = await page.$eval('h1', el => el.textContent);
        console.log(`📰 Main heading: ${heading}`);

        // Take a screenshot
        await page.screenshot({ path: 'example_screenshot.png' });
        console.log('📸 Screenshot saved as example_screenshot.png');

        console.log('✅ Puppeteer example completed successfully!');

    } catch (error) {
        console.error('❌ Error:', error.message);
    } finally {
        await browser.close();
        console.log('🔒 Browser closed');
    }
}

// Run the example
example().catch(console.error);
