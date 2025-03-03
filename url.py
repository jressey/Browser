import ssl
import socket
import io

STANDARD_HEADERS = [
    "Connection: keep-alive\r\n",
    "User-Agent: SwagBroLite\r\n",
]

class URL:
    def __init__(self, url):
        self.configured_socketcheme, url = url.split("://", 1)
        
        # append so url = "example.com" becomes "example.com/"
        if "/" not in url:
            url += "/"
        self.host, url = url.split("/", 1)
        
        # handle custom port
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

        self.configured_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        # enables theoretical reuse of the socket
        self.configured_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def submit_request(self):

        print("Making request to:\r\n{}".format(self.request))
        
        try:
            self.configured_socket.connect((self.host, self.port))
        except OSError:
            print("Socket already connected")
        
        self.configured_socket.send(self.request.encode("utf-8"))
        response = self.configured_socket.makefile("rb")
        plain_response = io.TextIOWrapper(response, encoding='utf-8', newline="\r\n")
        response_headers = {}
        while True:
            line = plain_response.readline()
            print(line)
            if line == "\r\n":
                break
            try:
                header, value = line.split(":", 1)
                if header.lower() == "content-length":
                    self.content_length = int(value.strip())
                    response_headers[header.lower()] = value.strip()
            except ValueError:
                print("The line: \"{}\" was ignored as a header".format(line.strip()))
                continue

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        return plain_response.read(self.content_length)
    
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
