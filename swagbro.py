import sys
from url import HttpURL, HttpsURL
from file_url import FileURL
from body_printer import BodyPrinter
from web_request_scheme_selector import WebRequestSchemeSelector

lookups = {}

def load(url):
    body = url.submit_request()
    BodyPrinter(body, is_view_source).print()

if __name__ == "__main__":
    i = 2
    while i > 0:
        i = i - 1
        raw_url = sys.argv[1]
        web_request_scheme_selector = WebRequestSchemeSelector(raw_url)
        is_view_source = web_request_scheme_selector.is_view_source
        if is_view_source: 
            raw_url = raw_url.replace("view-source:", "") 
        scheme = web_request_scheme_selector.select()
        
        if raw_url in lookups:
            if scheme == "data":
                BodyPrinter(lookups[raw_url]).print()
            else:
                load(lookups[raw_url])
        elif scheme == "http":
            http_url = HttpURL(raw_url)
            lookups[raw_url] = http_url
            load(http_url)
        elif scheme == "https":
            https_url = HttpsURL(raw_url)
            lookups[raw_url] = https_url
            load(https_url)
        elif scheme == "file":
            file_url = FileURL(raw_url)
            load(file_url)
        elif scheme == "data":
            data_content = raw_url.split(",", 1)[1].strip()
            lookups[raw_url] = data_content
            BodyPrinter(data_content).print()
        else:
            raise ValueError("Unknown scheme")
        

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