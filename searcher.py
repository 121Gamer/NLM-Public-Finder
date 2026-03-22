from ddgs import DDGS
import time
import random
import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# Regex to match a NotebookLM public URL
NLM_URL_PATTERN = re.compile(r'https://notebooklm\.google\.com/notebook/[a-zA-Z0-9_-]+')

def clean_title(raw_title, url):
    """Strip common NotebookLM suffixes and fall back to URL."""
    title = (raw_title or '').strip()
    for suffix in [' - NotebookLM', ' | NotebookLM',
                   ' - Google NotebookLM', ' \u2013 NotebookLM']:
        if title.endswith(suffix):
            title = title[: -len(suffix)].strip()
    return title or url


def fetch_page_meta(url):
    """Fallback: scrape title + description directly from the page."""
    try:
        response = requests.get(url, timeout=7, headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            raw_title = soup.title.string.strip() if soup.title else ''
            title = clean_title(raw_title, url)
            desc_tag = (
                soup.find('meta', attrs={'name': 'description'}) or
                soup.find('meta', attrs={'property': 'og:description'})
            )
            description = (
                desc_tag['content'].strip()
                if desc_tag and desc_tag.get('content') else ''
            )
            return title, description
    except Exception:
        pass
    return url, ''


def extract_notebook_urls_from_page(url_or_text, is_url=True):
    """Finds all notebook links inside a given web page or text snippet."""
    found = set()
    if not is_url:
        found.update(NLM_URL_PATTERN.findall(url_or_text))
        return found
        
    try:
        resp = requests.get(url_or_text, timeout=5, headers=HEADERS)
        if resp.status_code == 200:
            found.update(NLM_URL_PATTERN.findall(resp.text))
    except Exception:
        pass
    return found


def translate_query(user_query):
    """
    DDG doesn't index public NotebookLM links natively.
    Instead, we do a Deep Extraction search: we search for pages 
    MENTIONING the base URL, then scrape those pages for the real links.
    """
    q = user_query.strip()
    
    # Strip site: operator since we don't use it anymore
    q = re.sub(r'site:\S+\s*', '', q, flags=re.IGNORECASE).strip()
    
    base_search = '"notebooklm.google.com/notebook/"'
    if q:
        return f"{base_search} {q}"
    return base_search


def search_notebooks_robust(query="", num_results=10):
    """
    Two-step deep extraction search.
    1. Finds blogs, forums, and articles mentioning NotebookLM public links.
    2. Scrapes them to extract the actual notebook links.
    3. Fetches the title & description of each discovered notebook.
    """
    results = []
    seen_urls = set()

    ddg_query = translate_query(query)
    print(f"DDG extraction query: '{ddg_query}' | want={num_results}")

    with DDGS() as ddgs:
        # Step 1: Search DDG for mentions
        raw_pages = list(ddgs.text(ddg_query, max_results=num_results + 5))
        print(f"  DDG returned {len(raw_pages)} source pages")

        for item in raw_pages:
            source_url = item.get('href', '').strip()
            source_title = item.get('title', '').strip()
            source_body = item.get('body', '').strip()
            
            if not source_url:
                continue
                
            print(f"  Scanning source: {source_url[:60]}")
            
            # Step 2: Extract real notebook URLs from the snippet and the page
            notebook_links = extract_notebook_urls_from_page(source_body, is_url=False)
            notebook_links.update(extract_notebook_urls_from_page(source_url, is_url=True))
            
            # Step 3: Process the discovered notebooks
            for nb_url in notebook_links:
                if nb_url in seen_urls:
                    continue
                seen_urls.add(nb_url)
                
                print(f"    Found notebook: {nb_url}")
                title, description = fetch_page_meta(nb_url)
                
                # If Google redirects to sign-in, we use the context of the page where we found it!
                if "Sign in - Google Accounts" in title or title == nb_url or not title:
                    title = f"Notebook from: {source_title}" if source_title else nb_url
                    description = source_body
                
                results.append({
                    'title': title, 
                    'url': nb_url, 
                    'description': description
                })
                
                if len(results) >= num_results:
                    break
                    
            if len(results) >= num_results:
                break
                
            time.sleep(random.uniform(0.3, 0.8))

    print(f"  -> Collected {len(results)} notebooks.")
    return results
