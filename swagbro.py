import sys
from url import HttpURL, HttpsURL, FileURL

def show(body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url):
    body = url.submit_request()
    show(body)

if __name__ == "__main__":
    raw_url = sys.argv[1]
    scheme = ""
    data_content = ""

    if raw_url.startswith("data:"):
        scheme = "data"
        data_content = raw_url.split(",", 1)[1].strip()
    else:
        scheme = raw_url.split("://", 1)[0]
    
    if scheme == "http":
        load(HttpURL(raw_url))
    elif scheme == "https":
        load(HttpsURL(raw_url))
    elif scheme == "file":
        load(FileURL(raw_url))
    elif scheme == "data":
        show(data_content)
    else:
        raise ValueError("Unknown scheme")