const path = require('path');
const { expect } = require('chai');
const chai = require('chai');
const { test } = require('./browser');
chai.use(require('chai-fs'));

const URL = 'https://psalms.stcsfc.org';

const SELS = {
  heading: 'h1',
  getStarted: '#get-started',
  plainText: '#plain-text',
  pdf: '#pdf',
  propresenter: '#propresenter',
  download: '#click-to-download',
};

describe('psalms.stcsfc.org', () => {
  it(
    'heading on page',
    test(async browser => {
      const page = await browser.newPage();
      await page.goto(URL);
      await page.waitFor(SELS.heading);

      const innerText = await page.evaluate(sel => {
        return document.querySelector(sel).innerText;
      }, SELS.heading);
      expect(innerText).to.be.equal('Psalms for Screens');
    })
  );

  it(
    'get started button on page',
    test(async browser => {
      const page = await browser.newPage();
      await page.goto(URL);
      await page.waitFor(SELS.getStarted);

      const innerText = await page.evaluate(sel => {
        return document.querySelector(sel).innerText;
      }, SELS.getStarted);
      expect(innerText).to.be.equal('Get Started');
    })
  );

  it(
    'plain text download',
    test(async browser => {
      const page = await browser.newPage();
      await page.goto(URL);
      await page._client.send('Page.setDownloadBehavior', {
        behavior: 'allow',
        downloadPath: path.resolve(__dirname),
      });
      // click get started button
      await page.waitFor(SELS.getStarted);
      await page.click(SELS.getStarted);
      // check plain text button is there
      await page.waitFor(SELS.plainText);
      const innerText = await page.evaluate(sel => {
        return document.querySelector(sel).innerText;
      }, SELS.plainText);
      expect(innerText).to.be.equal('Plain Text');
      // click plain text button
      await page.click(SELS.plainText);
      // wait for and click download button
      await page.waitFor(SELS.download);
      const innerTextDownload = await page.evaluate(sel => {
        return document.querySelector(sel).innerText;
      }, SELS.download);
      expect(innerTextDownload).to.be.equal('Click to download your Psalms');

      await page.click(SELS.download);

      expect('PlainText.zip').to.be.a.path();
    })
  );
});
