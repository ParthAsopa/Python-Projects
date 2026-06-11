# Statver — Headless Server Telemetry Dashboard

> A lightweight Python Discord bot that broadcasts live hardware metrics from a bare-metal Linux server to a dedicated Discord channel.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-Latest-5865F2?logo=discord&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Ubuntu%20%7C%20Debian-E95420?logo=ubuntu&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

Statver is designed specifically for **headless server environments** — repurposed laptops, mini-PCs, and similar bare-metal setups — where running a desktop monitoring GUI isn't viable. Instead of heavyweight dashboards, it reads CPU, RAM, thermals, battery state, and mount storage directly from the Linux `/sys/class/` filesystem and `psutil`, then pushes a clean embed to Discord every 2 minutes.

---

## Features

- **Live-Updating Dashboard** — Edits a single pinned embed on an interval rather than flooding the channel with new messages.
- **Direct Hardware Polling** — Reads battery state and CPU thermal zones straight from the Linux kernel's `/sys/class/` interface, no additional drivers required.
- **Targeted Storage Monitoring** — Tracks a specific mount point (e.g. a Samba share) rather than just the root OS partition.
- **Production-Grade Deployment** — Ships with a `systemd` unit file so it runs as a background daemon, survives reboots, and auto-restarts on failure.
- **Secure Credential Handling** — API token and channel ID are kept out of source code via `python-dotenv`.
- **Low Battery Alerts** — Automatically pings the server manager when battery falls below 20%, with escalating notifications at 20%, 15%, 10%, then every 2 minutes until charging resumes.

---

## Tech Stack

| Component           | Details               |
| ------------------- | --------------------- |
| Language            | Python 3.14           |
| Discord Integration | `discord.py`          |
| System Metrics      | `psutil`              |
| Secrets Management  | `python-dotenv`       |
| Target OS           | Ubuntu / Debian Linux |

---

## Installation

### 1. Prerequisites

- Python 3.14 installed and accessible on your `PATH`
- A Discord Bot Token from the [Discord Developer Portal](https://discord.com/developers/applications)
- **Important:** Enable the **Message Content Intent** in your bot's portal settings — Statver needs it to read and edit the dashboard embed

### 2. Clone the Repository

```bash
git clone https://github.com/ParthAsopa/Python-Projects.git
cd python-projects/Statver
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
nano .env
```

Add the following, replacing the placeholder values with your own:

```env
STATVER_DISCORD_TOKEN=your_bot_token_here
STATVER_CHANNEL_ID=your_discord_channel_id_here
STATVER_STORAGE_PATH=/srv/CloudDrive
SERVER_MANAGER_ID=your_server_manager_user_id_here
```

| Variable                | Description                                                       |
| ----------------------- | ----------------------------------------------------------------- |
| `STATVER_DISCORD_TOKEN` | Your bot's secret token from the Developer Portal                 |
| `STATVER_CHANNEL_ID`    | The ID of the Discord channel to post the dashboard in            |
| `STATVER_STORAGE_PATH`  | The mount point you want to track (e.g. your Samba share)         |
| `SERVER_MANAGER_ID`     | Discord user ID of the server manager to ping when battery is low |

---

## Usage

### Running Manually (Development / Testing)

```bash
python3.14 statver.py
```

Press `Ctrl + C` to stop. Use this to verify the bot connects and the embed posts correctly before deploying as a service.

---

## Production Deployment (systemd)

Running Statver as a `systemd` service keeps it alive across reboots, SSH disconnects, and crashes.

**Step 1 — Create the service unit file:**

```bash
sudo nano /etc/systemd/system/statver.service
```

**Step 2 — Paste the following configuration:**

> Replace `/home/user/Statver` with the actual absolute path to your deployment directory, and `your_linux_username` with your system username.

```ini
[Unit]
Description=Statver Discord Telemetry Dashboard
After=network.target

[Service]
Type=simple
User=your_linux_username
WorkingDirectory=/home/user/Statver
ExecStart=/usr/bin/python3.14 /home/user/Statver/statver.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Step 3 — Enable and start the daemon:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable statver
sudo systemctl start statver
```

**Step 4 — Verify it's running:**

```bash
sudo systemctl status statver
```

---

## Troubleshooting

**Dashboard embed isn't updating even though the bot is online**

Verify the bot has the following permissions in the target channel:

- `Send Messages`
- `Read Message History`
- `Manage Messages`

---

**Battery or Temperature shows `N/A`**

Different hardware manufacturers expose sensors at different paths in `/sys/class/`. Check what your server exposes:

```bash
# List available battery nodes
ls /sys/class/power_supply/

# List available thermal zones
ls /sys/class/thermal/
```

If your device uses `BAT1` instead of `BAT0`, or `thermal_zone1` instead of `thermal_zone0`, update the paths inside the `get_battery()` and `get_temperature()` functions in `statver.py` accordingly.

---

## Project Structure

```
Statver/
├── statver.py          # Main bot entry point
├── requirements.txt    # Python dependencies
├── .env                # Secrets (not committed to version control)
└── .env.example        # Template for environment variables
```

---

## License

This project is licensed under the MIT License.
