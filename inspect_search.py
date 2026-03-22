import googlesearch
import inspect

print(f"googlesearch version: {googlesearch.__version__ if hasattr(googlesearch, '__version__') else 'unknown'}")
print(f"search function signature: {inspect.signature(googlesearch.search)}")
print(f"search function doc: {googlesearch.search.__doc__}")
