import ssl
import socket
import io
from web_request_handler import WebRequestHandler

class RedirectException(Exception):
    def __init__(self, redirect_url):
        self.redirect_url = redirect_url

STANDARD_HEADERS = [
    "Connection: keep-alive\r\n",
    "User-Agent: SwagBroLite\r\n",
]

class URL:
    def __init__(self, url):
        self.content_length = 1000
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
        # enables reuse of the socket
        self.configured_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def submit_request(self):
        redirect_url = None
        is_redirect = False

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
            # check for redirect
            if "301 Moved Permanently" in line:
                print("Redirecting")
                is_redirect = True
            if line == "\r\n":
                break
            try:
                header, value = line.split(":", 1)
                # get redirect url if present
                if header.lower() == "location":
                    redirect_url = value.strip()
                    raise RedirectException(redirect_url)
                if header.lower() == "content-length":
                    self.content_length = int(value.strip())
                    response_headers[header.lower()] = value.strip()
            except ValueError as e:
                continue

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        if is_redirect:
            WebRequestHandler().load(HttpURL(redirect_url), False)
            # make a new call
            print(redirect_url)
            pass
        else:    
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
        try:
            ctx = ssl.create_default_context()
            self.configured_socket = ctx.wrap_socket(self.configured_socket, server_hostname=self.host)
        except:
            print("Socket already wrapped")
        return super().submit_request()
    