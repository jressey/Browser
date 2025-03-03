class FileURL:
    def __init__(self, url):
        self.url = url.replace("file://", "")
        self.file = open(self.url, "r")
        self.file.seek(0)
        
    def submit_request(self):
        return self.file.read()