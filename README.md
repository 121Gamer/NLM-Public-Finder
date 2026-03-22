# 📚 NLM Public Finder

**Discover, curate, and explore publicly shared Google NotebookLM notebooks across the web.**

![NLM Public Finder UI](https://github.com/121Gamer/NLM-Public-Finder/blob/main/.ai/screenshot_placeholder.jpg?raw=true)

## 🌟 Overview

Google NotebookLM is an incredible tool for AI-assisted research, but there is no native central repository for finding public notebooks created by others. Furthermore, searching Google for `site:notebooklm.google.com` often yields limited results due to rate-limiting and Google's bot protections (which redirect automated requests to a Sign-In wall).

**NLM Public Finder** solves this by using a "Deep Extraction" technique via DuckDuckGo. It searches the web for blogs, Reddit threads, and forums that *mention* public notebooks, scrapes those pages to extract the actual `notebooklm.google.com/notebook/X` URLs, and automatically assigns them the title and description from the context in which they were shared.

The result is a fast, rate-limit-free, premium local library of public notebooks.

---

## ✨ Features

- **Deep Extraction Search Engine**: Uses DuckDuckGo to bypass Google's strict rate limits and auth-walls, finding notebooks mentioned anywhere on the internet.
- **Premium Glassmorphism UI**: A stunning dark-mode interface built with Vanilla CSS/JS.
- **Local SQLite Library**: Saves your discovered notebooks locally (`notebooks.db`) so you never lose them. No duplicates.
- **Smart Filtering & Pagination**: Instantly filter your library by title, URL, description, or tags without page reloads.
- **Tagging System**: Add custom comma-separated tags to any notebook to keep your library organized.
- **Export to CSV**: Download your entire curated library with one click.
- **Privacy First**: Fully local Flask backend. No accounts, no telemetry, no API keys required.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/121Gamer/NLM-Public-Finder.git
   cd NLM-Public-Finder
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:
   **http://127.0.0.1:5000**

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, SQLite3
- **Search Engine**: `ddgs` (DuckDuckGo Search), `requests`, `BeautifulSoup4`
- **Frontend**: HTML5, Vanilla CSS (Glassmorphism), Vanilla JavaScript, Google Fonts (Inter)

---

## 💡 How it works (The Deep Extraction Method)
Because Google redirects automated HTTP requests for `notebooklm.google.com/notebook/*` to a login screen, standard scraping tools fail to extract the title and description of a public notebook.

NLM Public Finder bypasses this by observing the context where the notebook was shared:
1. It queries DuckDuckGo for `notebooklm.google.com/notebook/` alongside your keywords.
2. It fetches the source pages (blogs, forums).
3. It parses the body text for notebook links via regex.
4. It extracts the title and description from the source page itself, attributing it back to the notebook URL.

---

## 🔒 Security
No API keys or sensitive data are required to run this project. `app.secret_key` uses a safe local default for Flask sessions but can be overridden in production via the `SECRET_KEY` environment variable. The SQLite database `notebooks.db` is successfully `.gitignored` to prevent your personal library from being accidentally committed.

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

---
*Disclaimer: Not affiliated with Google or NotebookLM. This is an independent, open-source tool built to help the community share and discover research.*
