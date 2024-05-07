import sys
from html.parser import HTMLParser

html = sys.argv[1]
print(html)

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.if_status = False
        self.status = []

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for k, v in attrs:
                if k == "class" and "alert "in v:
                    self.if_status = True

    def handle_endtag(self, tag):
        if self.if_status:
            self.if_status = False

    def handle_data(self, data):
        if self.if_status:
            self.status.append(data)

with open(html) as file:
    parser = MyHTMLParser()
    parser.feed(file.read())
    print(" ".join(parser.status[-1].split()))
