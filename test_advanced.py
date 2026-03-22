from googlesearch import search

print("Testing advanced search...")
try:
    results = search("python", num_results=3, advanced=True, sleep_interval=1)
    for result in results:
        print(f"Type: {type(result)}")
        print(f"Result: {result}")
        if hasattr(result, 'title'):
            print(f"Title: {result.title}")
        if hasattr(result, 'url'):
            print(f"URL: {result.url}")
        if hasattr(result, 'description'):
            print(f"Description: {result.description}")
except Exception as e:
    print(f"Error: {e}")
