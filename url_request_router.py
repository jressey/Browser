from url import HttpsURL, HttpURL
from file_url import FileURL
from body_printer import BodyPrinter
from web_request_scheme_selector import WebRequestSchemeSelector

class UrlRequestRouter:
    def __init__(self, raw_url, lookups, web_request_handler):
        self.raw_url = raw_url
        self.lookups = lookups
        self.web_request_handler = web_request_handler

        web_request_scheme_selector = WebRequestSchemeSelector(self.raw_url)
        self.is_view_source = web_request_scheme_selector.is_view_source
        if self.is_view_source: 
            self.raw_url = self.raw_url.replace("view-source:", "") 
        self.scheme = web_request_scheme_selector.select()

    def process(self):
        if self.raw_url in self.lookups:
            if self.scheme == "data":
                BodyPrinter(self.lookups[self.raw_url]).print()
            else:
                self.web_request_handler.load(self.lookups[self.raw_url], self.is_view_source)

        self.assign_url_object()
        self.process_request()
    
    def assign_url_object(self):
        if self.scheme == "http":
            self.url = HttpURL(self.raw_url)
        elif self.scheme == "https":
            self.url = HttpsURL(self.raw_url)
        elif self.scheme == "file":
            self.url = FileURL(self.raw_url)
        elif self.scheme == "data":
            self.url = None
        else:
            raise ValueError("Unknown scheme")
    
    def process_request(self):
        if self.scheme == "data":
            self.process_data()
        else:
            self.web_request_handler.load(self.url, self.is_view_source)
    
    def process_data(self):
        data_content = self.raw_url.split(",", 1)[1].strip()
        self.lookups[self.raw_url] = data_content
        BodyPrinter(data_content).print()