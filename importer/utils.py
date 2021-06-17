class URLParser:
    def __init__(self, url=None):
        self.url_parts = []
        if url:
            self.url_parts = url.strip("/").split("/")
        else:
            print("url is required!")

    def find_slug(self):
        return "".join(self.url_parts[-1:])
