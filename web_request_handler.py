from body_printer import BodyPrinter

class WebRequestHandler:
    def load(self, url, is_view_source):
        body = url.submit_request()
        print(body)
        BodyPrinter(body, is_view_source).print()
