# 🚀 How to connect Selenium grid with Playwright for scraping using Python, JS and Go.

This project demonstrates how to orchestrate a scalable web scraping infrastructure using **Docker Compose**, **Selenium Grid**, and **Playwright**. It includes implementations in **Python**, **Go**, and **JavaScript**.

---

## 📺 Video Tutorial

I've created a full walkthrough explaining the architecture, the setup, and the code logic.
👉 [Watch the Video on YouTube](https://youtu.be/OT06-RDFkrI)

---

## 🛠️ Tech Stack

- **Orchestration:** Docker & Docker Compose
- **Infrastructure:** Selenium Grid (Hub & Nodes)
- **Automation:** Playwright (Cross-language support)
- **Languages:** Python 🐍, Go 🐹, JavaScript ⚡

---

## 🏗️ Architecture

The setup consists of a **Selenium Hub** acting as a traffic distributor and multiple **Chrome/Firefox nodes** running in containers. This allows us to scale our scraping capabilities horizontally.

---

## 🚀 How to Run

### 1. Start the Infrastructure

Make sure you have Docker installed. Run the following command in the root directory:

```bash
docker-compose up -d --build
```

### 🐍 Python (using uv)

```bash
cd python
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

python pw_env.py  # Environment variable method
python pw_cdp.py  # CDP method
```

### ⚡ JavaScript (Node.js)

```bash
cd js
npm install
node pw_cdp.js
```

### 🐹 Golang

```bash
cd go
go mod tidy
go run github.com/playwright-community/playwright-go/cmd/playwright@latest install --with-deps
go run main.go
```
