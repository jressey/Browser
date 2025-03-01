import ssl
import socket

class URL:
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        if "/" not in url:
            url += "/"
        self.host, url = url.split("/", 1)
        
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)
        self.path = "/" + url

        if self.host == "":
            self.host = "localhost"

        self.headers = []
        self.headers.append("Host: {}\r\n".format(self.host))
        self.headers.append("Connection: close\r\n")
        self.headers.append("User-Agent: SwagBroLite\r\n")

    def request(self):

        request = "GET {} HTTP/1.1\r\n".format(self.path)
        
        for header in self.headers:
            request += header

        request += "\r\n"

        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )

        print(request)

        s.connect((self.host, self.port))
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
        
        s.send(request.encode("utf-8"))

        response = s.makefile("r", encoding="utf-8", newline="\r\n")

        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            response_headers[header.lower()] = value.strip()

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        content = response.read()
        s.close()

        return content
        
class HttpURL(URL):
    def __init__(self, url):
        super().__init__(url)
        self.port = 80

    def request(self):
        return super().request()

class HttpsURL(URL):
    def __init__(self, url):
        super().__init__(url)
        self.port = 443

    def request(self):
        return super().request()

class FileURL(URL):
    def __init__(self, url):
        super().__init__(url)
        self.port = 8000

    def request(self):
        return super().request()

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
    body = url.request()
    show(body)

if __name__ == "__main__":
    import sys
    scheme = sys.argv[1].split("://", 1)[0]
    print(scheme)
    if scheme == "http":
        load(HttpURL(sys.argv[1]))
    elif scheme == "https":
        load(HttpsURL(sys.argv[1]))
    elif scheme == "file":
        load(FileURL(sys.argv[1]))
    else:
        raise ValueError("Unknown scheme")