# 🚀 Anonymous Web Scraping: Playwright & Requests via Tor

This project demonstrates how to perform anonymous web scraping using **Python** with two different approaches: **Playwright** (for dynamic, JS-heavy sites) and **Requests** (for fast, headful API/HTML scraping). Both methods are routed through the **Tor Network** using Docker.

---

## 📺 Video Tutorial

I've created a full walkthrough explaining the architecture or the proxy configuration differences as well as using it with requests and playwright.
👉 [Watch the Video on YouTube](https://youtu.be/YOUR_VIDEO_ID)

---

## 🛠️ Tech Stack

- **HTTP Client:** Requests (with SOCKS support) 🌐
- **Automation:** Playwright (Connected to selenium grid) 🎭
- **Anonymity:** Tor Network 🧅
- **Orchestration:** Docker & Docker Compose 🐳

---

## 🏗️ Architecture & Proxy Logic

The project uses a **Dockerized Tor** container as a gateway. A key part of this tutorial is understanding the protocol difference:

* **Requests (`socks5h://`):** We use the `h` extension to ensure **DNS resolution** happens on the proxy side (Tor), preventing your real IP from leaking via DNS queries.
* **Playwright (`socks5://`):** The browser context handles the routing. We point it to the SOCKS5 endpoint to tunnel all navigation traffic.

---

## 🚀 How to Run

### 1. Spin up the Tor Proxy
Make sure Docker is running, then start the Tor service:

```bash
docker-compose up -d --build
```

### 🐍 Python (using uv)

```bash
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

uv pip install -r requirements.txt
playwright install chromium

python requests_example.py  # Using SOCKS5h
python pw_example.py        # Using SOCKS5
```