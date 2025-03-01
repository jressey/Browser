import ssl
import socket

STANDARD_HEADERS = [
    "Connection: close\r\n",
    "User-Agent: SwagBroLite\r\n",
]

class URL:
    def __init__(self, url):
        self.configured_socketcheme, url = url.split("://", 1)
        # append so
        # url = "example.com" becomes "example.com/"
        if "/" not in url:
            url += "/"
        self.host, url = url.split("/", 1)
        
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)
        self.path = "/" + url

        # assume localhost
        if self.host == "":
            self.host = "localhost"

        self.request = "GET {} HTTP/1.1\r\n".format(self.path)
        
        self.request += "Host: {}\r\n".format(self.host)
        for header in STANDARD_HEADERS:
            self.request += header

        self.request += "\r\n"

        print("Making request to:\r\n{}".format(self.request))

        self.configured_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )

    def submit_request(self):

        self.configured_socket.connect((self.host, self.port))
        self.configured_socket.send(self.request.encode("utf-8"))
        response = self.configured_socket.makefile("r", encoding="utf-8", newline="\r\n")

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            try:
                header, value = line.split(":", 1)
                response_headers[header.lower()] = value.strip()
            except ValueError:
                print("The line: \"{}\" was ignored as a header".format(line.strip()))
                continue

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        content = response.read()
        self.configured_socket.close()

        return content
        
class HttpURL(URL):
    def __init__(self, url):
        self.port = 80
        super().__init__(url)

    def submit_request(self):
        return super().submit_request()

class HttpsURL(URL):
    def __init__(self, url):
        self.port = 443
        super().__init__(url)

    def submit_request(self):
        ctx = ssl.create_default_context()
        self.configured_socket = ctx.wrap_socket(self.configured_socket, server_hostname=self.host)
        return super().submit_request()

class FileURL(URL):
    def __init__(self, url):
        self.port = 8000
        super().__init__(url)

    def submit_request(self):
        return super().submit_request()

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