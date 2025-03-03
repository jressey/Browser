class WebRequestSchemeSelector:
    def __init__(self, raw_url):
        self.raw_url = raw_url
        self.is_view_source = self.raw_url.startswith("view-source:")

        if self.is_view_source:
            self.raw_url = self.raw_url.replace("view-source:", "")
        
    def select(self):
        if self.raw_url.startswith("data:"):
            return "data"
        else:
            return self.raw_url.split("://", 1)[0]