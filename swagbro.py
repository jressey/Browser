import sys
from url import HttpURL, HttpsURL, FileURL
from body_printer import BodyPrinter
from web_request_scheme_selector import WebRequestSchemeSelector

def load(url):
    body = url.submit_request()
    BodyPrinter(body).print()

if __name__ == "__main__":
    raw_url = sys.argv[1]
    scheme = WebRequestSchemeSelector(raw_url).select()
    
    if scheme == "http":
        load(HttpURL(raw_url))
    elif scheme == "https":
        load(HttpsURL(raw_url))
    elif scheme == "file":
        load(FileURL(raw_url))
    elif scheme == "data":
        data_content = raw_url.split(",", 1)[1].strip()
        BodyPrinter(data_content).print()
    else:
        raise ValueError("Unknown scheme")