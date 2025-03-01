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
    import sys
    scheme = sys.argv[1].split("://", 1)[0]
    if scheme == "http":
        load(HttpURL(sys.argv[1]))
    elif scheme == "https":
        load(HttpsURL(sys.argv[1]))
    elif scheme == "file":
        load(FileURL(sys.argv[1]))
    else:
        raise ValueError("Unknown scheme")