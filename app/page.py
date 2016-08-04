import os
import re

from flask_misaka import markdown


def parse_path(path, md=True):
    path = os.path.splitext(path)[0]
    if path == "":
        path = "index"
    if md:
        return "pages/" + path + ".md"
    else:
        return "pages/" + path

class Page:
    metadata = re.compile(r'(^@\s*(.*(?:[ \t]{2,}.*)*)\n)', re.MULTILINE)

    def __init__(self, path):  # change to file itself

        self.name = path
        self.time = None
        self.markdown = self.load_file(
        )
        self.markup = None
        self.title = None
        self.author = None
        self.date = None
        self.parse()

    def parse(self):
        self.markdown = self.parse_metadata(self.markdown)
        self.markup = markdown(self.markdown, strikethrough=True, autolink=True, fenced_code=True, highlight=True,
                               quote=True, math=True, superscript=True, tables=True, footnotes=True, smartypants=True)

    def parse_metadata(self, raw_contents):
        matches = re.findall(self.metadata, raw_contents)
        self.title = matches[0][1] if matches[0:] else None
        self.author = matches[1][1] if matches[1:] else None
        self.date = matches[2][1] if matches[2:] else None
        for match in matches:
            raw_contents = raw_contents[len(match[0]):]
        return raw_contents

    def load_file(self):
        path = parse_path(self.name)
        if os.path.isfile(path):
            file = open(path)
            contents = file.read()
            self.time = os.path.getmtime(path)
            file.close()
            return contents
        self.title = "404"
        return "##404##"


