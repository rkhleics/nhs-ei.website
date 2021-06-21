import requests
import requests_cache
import sys
import os

"""TODO: this should use the Django config but I haven't figured that out."""
# from django.conf import settings
# DEBUG = settings.DEBUG
DEBUG = True

CACHE_DB = "requests_cache.sqlite"

if "reset" in sys.argv:
    os.remove(CACHE_DB)
    print("Removed old HTTP cache.")

if DEBUG:
    session = requests_cache.CachedSession(CACHE_DB)
else:
    session = requests.session()

if __name__ == "__main__":
    print("Quick test: this should take 2 or 0 seconds")
    for i in range(5):
        session.get("http://httpbin.org/delay/2")
    print("Done.")
