import time

import requests
from stem import Signal
from stem.control import Controller

from utils import get_logger


class TorRetryError(Exception):
    """Raised when all retries has been consumed."""

    pass


class TorRequestsScraper:
    def __init__(self, tor_password="alpha", control_port=9051, proxy_port=9050):
        self.logger = get_logger("TorRequestsScraper")
        self.password = tor_password
        self.control_port = control_port
        self.proxies = {
            "http": f"socks5h://localhost:{proxy_port}",
            "https": f"socks5h://localhost:{proxy_port}",
        }
        self.logger.info("TorRequestsScraper initialized. Ready to route traffic.")

    def rotate_identity(self):
        with Controller.from_port(port=self.control_port) as controller:
            controller.authenticate(password=self.password)
            controller.signal(Signal.NEWNYM)
            self.logger.warning("Requesting new identity... Changing Tor circuit.")
            time.sleep(2)

    def request_with_retries(self, url, max_retries=5):
        for attempt in range(1, max_retries + 1):
            try:
                self.logger.info(f"Attempt {attempt}/{max_retries} | Accessing: {url}")
                response = requests.get(url, proxies=self.proxies, timeout=15)

                # In this case never is going to enter here
                if response.status_code in [403, 429]:
                    self.logger.error(
                        f"IP Flagged/Blocked (Status: {response.status_code}). Rotating IP..."
                    )
                    self.rotate_identity()
                    continue

                response.raise_for_status()
                self.logger.info("Successfully retrieved data!")
                return response

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Connection error: {e}. Attempting IP rotation...")
                self.rotate_identity()

        self.logger.critical(
            "Max retries reached. The target might be blocking Tor nodes."
        )
        raise TorRetryError(f"Failed to retry {url} after {max_retries} attempts.")


if __name__ == "__main__":
    scraper = TorRequestsScraper()
    target_url = "https://httpbin.org/ip"
    scraper.logger.info("--- STARTING ANONYMOUS SCRAPING SESSION ---")

    for i in range(2):
        if i == 1:
            scraper.logger.info("--- FORCING MANUAL ROTATION ---")
            scraper.rotate_identity()
        response = scraper.request_with_retries(target_url)
        html = response.text
        scraper.logger.info(f"Server response: {html}")
