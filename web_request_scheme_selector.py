class WebRequestSchemeSelector:
    def __init__(self, raw_url):
        self.raw_url = raw_url

    def select(self):
        if self.raw_url.startswith("data:"):
            return "data"
        else:
            return self.raw_url.split("://", 1)[0]