import os
import time

from playwright.sync_api import sync_playwright
from stem import Signal
from stem.control import Controller

from utils import get_logger

os.environ["SELENIUM_REMOTE_URL"] = "http://localhost:4444"
TOR_CONTROL_PORT = 9071
TOR_HOST = "tor_de"
TOR_PASSWORD = "alpha"
URL_TO_VISIT = "https://ipinfo.io/json"


class TorPlaywrightScraper:
    def __init__(
        self, tor_password="alpha", control_port=TOR_CONTROL_PORT, proxy_port=9050
    ):
        self.logger = get_logger("TorPlaywrightScraper")
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.proxy = f"socks5://{TOR_HOST}:{proxy_port}"
        self.password = tor_password
        self.control_port = control_port
        self.logger.info("TorPlaywrightScraper initialized.")

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--start-maximized"],
        )
        self.context = self.browser.new_context(
            no_viewport=True,
            proxy={"server": self.proxy},
        )
        self.page = self.context.new_page()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info("Cleaning up: Closing Playwright resources...")
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def run_playwright_task(self, url_to_visit: str):
        self.logger.info(f"🎬 Opening {url_to_visit}")
        self.page.goto(url_to_visit)
        self.logger.info(f"✅ Loaded: {self.page.title()}")
        return self.page.content()

    def rotate_identity(self):
        with Controller.from_port(port=self.control_port) as controller:
            controller.authenticate(password=self.password)
            controller.signal(Signal.NEWNYM)
            self.logger.warning("Requesting new identity... Changing Tor circuit.")
            time.sleep(2)

    def rotate_ip_with_playwright(self):
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        self.rotate_identity()
        self.context = self.browser.new_context(
            no_viewport=True, proxy={"server": self.proxy}
        )
        self.page = self.context.new_page()


if __name__ == "__main__":
    with TorPlaywrightScraper() as pw:
        pw.logger.info("--- STARTING ANONYMOUS PLAYWRIGHT SESSION ---")
        for i in range(2):
            if i == 1:
                pw.logger.info("--- FORCING MANUAL ROTATION ---")
                pw.rotate_ip_with_playwright()
            pw.logger.info(f"Iteration {i + 1}: Executing task...")
            content = pw.run_playwright_task(URL_TO_VISIT)
            pw.logger.info(f"Result iteration {i + 1}: {content}")
