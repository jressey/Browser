import sys
from url_request_router import UrlRequestRouter
from web_request_handler import WebRequestHandler

class SwagBro:
    def __init__(self, raw_url):
        self.raw_url = raw_url
        self.lookups = {}
        self.web_request_handler = WebRequestHandler()

    def process_url(self):
        processor = UrlRequestRouter(self.raw_url, self.lookups, self.web_request_handler)
        processor.process()

if __name__ == "__main__":
    raw_url = sys.argv[1]
    swagbro = SwagBro(raw_url)
    swagbro.process_url()
        

"""
Permutations:
- http://
- https://
- file:///
- data:
- view-source:http://
- view-source:https://
- view-source:file:///
- view-source:data:
"""