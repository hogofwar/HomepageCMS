import re
from flask_misaka import markdown


class Page:
    metadata = re.compile(r'(^@\s*(.*(?:\h{2,}.*)*)\n)', re.MULTILINE)

    def __init__(self, name, file_contents):
        self.name = name
        self.markdown = file_contents
        self.markup = None
        self.title = None
        self.author = None
        self.date = None
        self.parse()

    def parse(self):
        self.markdown = self.parse_metadata(self.markdown)
        self.markup = markdown(self.markdown, strikethrough=True)

    def parse_metadata(self, raw_contents):
        matches = re.findall(self.metadata, raw_contents)
        self.title = matches[0][1] if matches[0:] else None
        self.author = matches[1][1] if matches[1:] else None
        self.date = matches[2][1] if matches[2:] else None
        for match in matches:
            raw_contents = raw_contents[len(match[0]):]
        return raw_contents