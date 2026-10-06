const { chromium } = require('playwright');
const path = require('path');

(async () => {
    const htmlPath = path.resolve(__dirname, 'index.html');
    const targets = [
        { lang: 'en', pdfPath: path.resolve(__dirname, 'Samuel_Ishida_CV.pdf') },
        { lang: 'pt', pdfPath: path.resolve(__dirname, 'Samuel_Ishida_CV_pt.pdf') }
    ];

    const browser = await chromium.launch();

    for (const { lang, pdfPath } of targets) {
        const page = await browser.newPage();

        await page.goto('file://' + htmlPath, { waitUntil: 'networkidle' });

        // Force the desired language before printing (index.html persists to localStorage).
        await page.evaluate((l) => window.setLanguage(l), lang);

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

        await page.close();
        console.log('PDF generated:', pdfPath);
    }

    await browser.close();
})();
