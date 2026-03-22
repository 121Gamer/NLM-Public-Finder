# NLM Public Finder - AI Memory & Architecture

## Overview
This project is a Flask-based web application designed to find and curate public NotebookLM notebooks. Since Google's NotebookLM subdomains aren't indexed cleanly by standard search engines (and direct scrapes hit rate limits and Sign-In walls), this tool uses a "Deep Extraction" technique via DuckDuckGo.

## Core Architecture
1. **app.py**: The Flask backend. Exposes routes for `/` (UI), `/search` (executes DDG search), `/tag`, `/delete`, and `/stats`.
2. **searcher.py**: The brain of the operation. 
   - Uses the `ddgs` library (DuckDuckGo search) to find blogs, reddit posts, and forums that *mention* `notebooklm.google.com/notebook/`.
   - Scrapes the bodies of those results and the source URLs to extract the actual notebook links via regex.
   - Intelligently pulls titles and descriptions from the source page context (because directly hitting the Notebook URL redirects to a Google Sign-In wall).
3. **database.py**: SQLite persistence layer. Uses `notebooks.db` (gitignored). Stores URLs, extracted titles, descriptions, and user-defined tags. Includes an auto-migration method in `init_db()` to safely add columns.
4. **templates/index.html**: A premium, dark-mode, glassmorphism UI built with Vanilla JS and CSS. Features client-side filtering, pagination, AJAX tag saving, and live stats.

## Development History
- **Initial State**: Used `googlesearch-python` which got immediately rate-limited and failed to pull descriptions. UI was a plain HTML table.
- **V2 Upgrade**: Replaced backend with `ddgs`, implemented Deep Extraction, and built the premium card-based UI. Handled unicode Windows console errors (`charmap` failing on arrows).

## Future Directives for AI Agents
- **Do not use `googlesearch-python`**: It will fail with 429 Too Many Requests. Stick to `duckduckgo-search` (`ddgs`) or another keyless aggregator.
- **Do not fetch notebook URLs directly**: Google requires auth to view them. Always extract metadata from the referring page (the blog, forum, or tweet that shared it).
- **UI Adjustments**: Maintain the dark glassmorphism aesthetic (`--bg: #09090f`, `--surface: #12121d`). Any new interactive elements should prefer Vanilla JS (no heavy frameworks needed).
