const { Builder } = require("selenium-webdriver");
const chrome = require("selenium-webdriver/chrome");
const { chromium } = require("playwright");

const BASE = "localhost:4444";

async function runPlaywrightTask(cdpUrl, urlToVisit) {
  const browser = await chromium.connectOverCDP(cdpUrl);
  const defaultContext = browser.contexts()[0];
  let page = defaultContext.pages()[0] || (await defaultContext.newPage());

  console.log(`🎬 Navigating to ${urlToVisit}...`);
  await page.goto(urlToVisit, { waitUntil: "networkidle" });

  const title = await page.title();
  console.log(`✅ Loaded: ${title}`);
  await new Promise((resolve) => setTimeout(resolve, 2000));
  const content = await page.content();
  return { content, playwrightBrowser: browser, defaultContext, page };
}

class SeleniumGridBridge {
  constructor() {
    this.driver = null;
  }

  async init() {
    const options = this._getChromeOptions();
    this.driver = await new Builder()
      .usingServer(`http://${BASE}`)
      .forBrowser("chrome")
      .setChromeOptions(options)
      .build();
    return this;
  }

  _getChromeOptions() {
    const options = new chrome.Options();
    options.excludeSwitches("enable-automation");
    options.setUserPreferences({ useAutomationExtension: false });
    options.addArguments(
      "--enable-features=NetworkService,NetworkServiceInProcess",
      "--no-sandbox",
      "--disable-blink-features=AutomationControlled",
      "--start-maximized",
      "--no-first-run",
    );
    return options;
  }

  async getCdpUrl() {
    const session = await this.driver.getSession();
    return `ws://${BASE}/session/${session.getId()}/se/cdp`;
  }

  async cleanup() {
    if (this.driver) {
      console.log("Cleaning up: Closing Selenium driver...");
      await this.driver.quit();
    }
  }
}

(async () => {
  const bridge = new SeleniumGridBridge();
  let pwBrowser = null;
  let pwContext = null;
  let pwPage = null;
  try {
    await bridge.init();
    const cdpUrl = await bridge.getCdpUrl();
    const result = await runPlaywrightTask(cdpUrl, "https://www.github.com");
    content = result.content; 
    pwBrowser = result.playwrightBrowser;
    pwContext = result.context;
    pwPage = result.page;

    console.log("📄 Content length:", content.length);
  } catch (error) {
    console.error("An error has ocurred:", error);
  } finally {
    if (pwPage) await pwPage.close();
    if (pwContext) await pwContext.close();
    if (pwBrowser) await pwBrowser.close();

    await bridge.cleanup();
  }
})();
