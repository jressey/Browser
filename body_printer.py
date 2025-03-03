class BodyPrinter:
    def __init__(self, body):
        self.body = body
        self.printable = ""

    def clean_tags(self):
        self.printable = self.printable.replace("&lt;", "<")
        self.printable = self.printable.replace("&gt;", ">")

    def print(self):
        in_tag = False
        for c in self.body:
            if c == "<":
                in_tag = True
            elif c == ">":
                in_tag = False
            elif not in_tag:
                self.printable += c
        
        self.clean_tags()
        print(self.printable)
