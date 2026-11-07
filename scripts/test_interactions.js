const puppeteer = require('puppeteer-core');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true,
    defaultViewport: { width: 1440, height: 900 }
  });
  const page = await browser.newPage();
  page.on('console', msg => console.log('LOG:', msg.text()));
  page.on('pageerror', err => console.log('ERROR:', err.toString()));
  await page.goto('http://localhost:8080/index.html');
  await new Promise(r => setTimeout(r, 1000));

  // Test toggling every map metric button
  const buttons = await page.$$('#map-metric-buttons button');
  console.log('Found buttons:', buttons.length);
  for (let b of buttons) {
    const text = await (await b.getProperty('innerText')).jsonValue();
    console.log('Clicking button:', text);
    await b.click();
    await new Promise(r => setTimeout(r, 200));
  }

  // Test clicking on map paths
  const paths = await page.$$('#india-map path');
  console.log('Found SVG paths:', paths.length);
  if (paths.length > 0) {
    console.log('Clicking first 5 paths...');
    for (let i = 0; i < Math.min(paths.length, 5); i++) {
      await paths[i].click();
      await new Promise(r => setTimeout(r, 200));
    }
  }

  // Test filter dropdowns
  console.log('Testing zone filter...');
  await page.select('#zone-filter', 'South');
  await new Promise(r => setTimeout(r, 300));
  console.log('Testing state filter...');
  await page.select('#state-filter', 'Kerala');
  await new Promise(r => setTimeout(r, 300));

  console.log('Testing reset button...');
  await page.click('#reset-filters-btn');
  await new Promise(r => setTimeout(r, 300));

  console.log('All tests finished successfully!');
  await browser.close();
})();
