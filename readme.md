# Python Projects

A collection of personal Python projects spanning automation, web development, Discord bots, and utility tooling. This repository is a sandbox for learning, experimentation, and building practical things.

---

## Projects

### 1. Statver ([Statver/](Statver/))

A lightweight Discord bot that broadcasts a live-updating hardware telemetry dashboard for a headless bare-metal Linux server. Reads CPU, RAM, thermals, battery state, and storage directly from the Linux `/sys/class/` filesystem and `psutil`, posting a refreshed embed to Discord every 2 minutes. Deployed as a `systemd` background service.

**Stack:** Python · discord.py · psutil · python-dotenv

---

### 2. Selenium Automation ([Selenium/](Selenium/))

Learning and experimentation workspace for Selenium WebDriver-based browser automation.

**Sub-projects:**
- **WiFi Login Automation** ([`WiFi_Login/`](Selenium/WiFi_Login/)) — Automated hostel firewall login/logout using Edge WebDriver

**Key Files:**
- [`main.py`](Selenium/main.py) — Main experimentation entry point
- [`Automated Login.py`](Selenium/Automated%20Login.py) — Login automation scripts

---

### 3. Flask Web Application ([Flask/](Flask/))

A Flask-based web application with Jinja2 templating and static asset serving.

**Key Files:**
- [`temp.py`](Flask/temp.py) — Application entry point
- [`templates/index.html`](Flask/templates/index.html) — Web interface
- [`static/`](Flask/static/) — CSS, JS, and images

---

### 4. Lister ([Lister/](Lister/))

A simple list management CLI app with JSON-based persistence.

**Key Files:**
- [`main.py`](Lister/main.py) — Application logic
- [`lists.json`](Lister/lists.json) — Data storage

---

## Repository Structure

```
├── Statver/               # Discord telemetry bot
├── Flask/                 # Flask web app
├── Lister/                # List management utility
└── Selenium/              # Browser automation
    ├── WiFi_Login/
    └── selenium_libs/
```

---

*Each project runs independently. See the individual project folders for setup instructions.*