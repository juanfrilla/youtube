import time

from playwright.sync_api import sync_playwright
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE = "localhost:4444"


def run_playwright_task(cdp_url: str, url_to_visit: str):
    with sync_playwright() as p:
        print(f"🎬 Opening {url_to_visit}")
        browser = p.chromium.connect_over_cdp(cdp_url)
        if len(browser.contexts) == 0:
            context = browser.new_context(no_viewport=True)
            page = context.new_page()
        else:
            context = browser.contexts[0]
            page = context.pages[0] if len(context.pages) > 0 else context.new_page()
        page.goto(url_to_visit, wait_until="networkidle")

        print(f"✅ Loaded: {page.title()}")

        time.sleep(2)

        return page.content()


class SeleniumGridBridge:
    def __init__(self):
        chrome_options = self._get_chrome_options()
        self.driver = webdriver.Remote(
            command_executor=f"http://{BASE}", options=chrome_options
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            print("Cleaning up: Closing Selenium driver...")
            self.driver.quit()

    def _get_chrome_options(self) -> Options:
        chrome_options = Options()
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.headless = False
        arguments = [
            "--enable-features=NetworkService,NetworkServiceInProcess",
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
            "--no-first-run",
        ]
        for argument in arguments:
            chrome_options.add_argument(argument)
        return chrome_options

    def get_cdp_url(self) -> str:
        return f"ws://{BASE}/session/{self.driver.session_id}/se/cdp"


if __name__ == "__main__":
    with SeleniumGridBridge() as bridge:
        url_to_visit = "https://www.google.com"
        cdp_url = bridge.get_cdp_url()
        content = run_playwright_task(cdp_url, url_to_visit)
        print(content)
