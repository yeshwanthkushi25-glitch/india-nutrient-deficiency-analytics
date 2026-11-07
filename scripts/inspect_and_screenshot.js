const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

async function run() {
  const assetsDir = path.join(__dirname, '..', 'assets');
  if (!fs.existsSync(assetsDir)) fs.mkdirSync(assetsDir, { recursive: true });

  console.log('Launching Chrome...');
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true,
    defaultViewport: { width: 1440, height: 960, deviceScaleFactor: 2 } // 2x Retina quality
  });

  const page = await browser.newPage();

  console.log('Navigating to http://localhost:8080/index.html ...');
  await page.goto('http://localhost:8080/index.html', { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise(r => setTimeout(r, 2000));

  // 1. Full Page Screenshot
  const fullPagePath = path.join(assetsDir, 'full_dashboard.png');
  await page.screenshot({ path: fullPagePath, fullPage: true });
  console.log('Saved full dashboard screenshot to:', fullPagePath);

  // Helper to cleanly capture section without sticky headers overlapping
  async function captureCleanSection(selector, filename) {
    const el = await page.$(selector);
    if (!el) return;

    // Temporarily make sticky bars static for clean element framing
    await page.evaluate(() => {
      const nav = document.querySelector('.navbar');
      const filter = document.querySelector('.global-filter-bar');
      if (nav) nav.style.position = 'static';
      if (filter) filter.style.position = 'static';
    });

    await el.scrollIntoView();
    await new Promise(r => setTimeout(r, 400));

    const outPath = path.join(assetsDir, filename);
    await el.screenshot({ path: outPath });
    console.log(`Saved clean screenshot to: ${outPath}`);

    // Restore sticky positions
    await page.evaluate(() => {
      const nav = document.querySelector('.navbar');
      const filter = document.querySelector('.global-filter-bar');
      if (nav) nav.style.position = 'sticky';
      if (filter) filter.style.position = 'sticky';
    });
  }

  // 2. Executive KPI Deck
  await captureCleanSection('#executive-overview', 'executive_kpi_deck.png');

  // 3. Interactive Map & Scorecard Section
  await captureCleanSection('#choropleth-section', 'interactive_choropleth_map.png');

  // 4. Paradox & Demographic Charts
  await captureCleanSection('#analytics-charts', 'paradox_charts.png');

  // 5. Personal Plate Calculator
  await captureCleanSection('#calculator-section', 'plate_calculator.png');

  await browser.close();
  console.log('All screenshots captured cleanly at 2x resolution!');
}

run().catch(err => {
  console.error('Screenshot capture failed:', err);
  process.exit(1);
});
