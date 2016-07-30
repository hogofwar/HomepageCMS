import os
import re

from flask_misaka import markdown


class Page:
    metadata = re.compile(r'(^@\s*(.*(?:[ \t]{2,}.*)*)\n)', re.MULTILINE)

    def __init__(self, path):  # change to file itself

        self.name = path
        self.markdown = self.load_file(path)
        self.markup = None
        self.title = None
        self.author = None
        self.date = None
        self.time = None  # store last modified time of the file, if modified time is newer, regenerate
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

    def load_file(self, path):
        path = os.path.splitext(path)[0]
        if path == "":
            path = "index"
        if os.path.isfile("pages/" + path + ".md"):
            file = open("pages/" + path + ".md")
            contents = file.read()
            file.close()
            return contents
        return "##404##"
