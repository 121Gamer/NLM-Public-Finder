from googlesearch import search
import traceback

print("Starting search debug...")
try:
    query = "python"
    print(f"Searching for: {query}")
    count = 0
    for result in search(query, num=5, stop=5, pause=2.0):
        print(f"Result: {result}")
        count += 1
    print(f"Found {count} results.")
except Exception:
    traceback.print_exc()
print("Done.")
