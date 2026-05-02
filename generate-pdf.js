const { chromium } = require('playwright');
const path = require('path');

(async () => {
    const htmlPath = path.resolve(__dirname, 'index.html');
    const pdfPath = path.resolve(__dirname, 'Samuel_Ishida_CV.pdf');

    const browser = await chromium.launch();
    const page = await browser.newPage();

    await page.goto('file://' + htmlPath, { waitUntil: 'networkidle' });

    // Wait for fonts to load
    await page.waitForTimeout(2000);

    await page.pdf({
        path: pdfPath,
        format: 'A4',
        printBackground: true,
        margin: {
            top: '16mm',
            bottom: '16mm',
            left: '18mm',
            right: '18mm'
        }
    });

    await browser.close();
    console.log('PDF generated:', pdfPath);
})();
