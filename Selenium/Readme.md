# Selenium

## Overview

This folder is my learning workspace for Selenium, where I create and experiment with various web automation projects. It serves as a sandbox for exploring Selenium's capabilities and building practical automation solutions.

## Projects

### WiFi Login Automation

Located in [`WiFi_Login/`](WiFi_Login/)

An automated login and logout system for the hostel Wi-Fi firewall. This project demonstrates practical use of Selenium to streamline the connection process by automating credential entry and form submission.

**Features:**

- Automated firewall login via [`WiFi_Login.py`](WiFi_Login/WiFi_Login.py)
- Automated firewall logout via [`WiFi_Logout.py`](WiFi_Login/WiFi_Logout.py)
- Secure credential management via [`.env`](WiFi_Login/.env) file
- Easy-to-use batch file interface ([`Login.bat`](WiFi_Login/Login.bat), [`Logout.bat`](WiFi_Login/Logout.bat))
- Built with Selenium WebDriver and Edge browser

For more details, see [`WiFi_Login/Readme.md`](WiFi_Login/Readme.md).

### General Automation Scripts

- [`main.py`](main.py) - Main entry point for experimentation
- [`Automated Login.py`](Automated%20Login.py) - Additional login automation examples

## Project Structure

- **`selenium_libs/`** - Local virtual environment with Selenium dependencies
- **`WiFi_Login/`** - Dedicated WiFi automation sub-project

## Getting Started

Each project may have its own dependencies. Install Selenium using the local virtual environment or your preferred method:

```sh
pip install selenium
```

## Purpose

This is a learning and experimentation space. Projects range from simple scripts to more complex automation workflows as I continue to develop my Selenium expertise.

---

_Note: Projects in this folder are for personal use and experimentation._
