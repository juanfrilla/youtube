import os
import time

from playwright.sync_api import sync_playwright

os.environ["SELENIUM_REMOTE_URL"] = "http://localhost:4444"


class PlaywrightBrowser:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            channel="chrome", headless=False, args=["--start-maximized"]
        )
        if len(self.browser.contexts) == 0:
            self.context = self.browser.new_context(no_viewport=True)
            self.page = self.context.new_page()
        else:
            self.context = self.browser.contexts[0]
            self.page = (
                self.context.pages[0]
                if len(self.context.pages) > 0
                else self.context.new_page()
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Cleaning up: Closing Playwright resources...")
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def run_playwright_task(self, url_to_visit: str):
        print(f"🎬 Opening {url_to_visit}")
        self.page.goto(url_to_visit)
        print(f"✅ Loaded: {self.page.title()}")
        time.sleep(2)
        return self.page.content()


if __name__ == "__main__":
    with PlaywrightBrowser() as pw:
        url_to_visit = "https://www.google.com"
        content = pw.run_playwright_task(url_to_visit)
        print(content)
