from ddgs import DDGS
import re
import requests

ddgs = DDGS()
query = '"notebooklm.google.com/notebook/"'
print(f"Searching: {query}")
results = list(ddgs.text(query, max_results=5))

url_pattern = re.compile(r'https://notebooklm\.google\.com/notebook/[a-zA-Z0-9_-]+')

found_urls = set()

for r in results:
    body = r.get('body', '')
    matches = url_pattern.findall(body)
    for m in matches:
        found_urls.add(m)
        
    href = r.get('href')
    print(f"Fetching {href} to find links...")
    try:
        resp = requests.get(href, timeout=5)
        matches = url_pattern.findall(resp.text)
        for m in matches:
            found_urls.add(m)
    except Exception as e:
        print(f"  Error fetching: {e}")

print("\nFound Notebook Links:")
for url in found_urls:
    print(url)
