import os, json
from base64 import b64encode


class Config:

    def __init__(self, name):
        self.name = name
        self.save(name)
        self.config = {}

    def get(self, key):
        return self.config[key]

    def set(self, key, value, save=False):
        self.config[key] = value
        if save:
            self.save()

    def set(self, pairs, save=False):
        for (key, value) in pairs:
            self.set(key, value, False)
        if save:
            self.save()

    def load(self):
        if not os.path.isfile(self.name+".json"):
            self.load_defaults()
            self.save()

        with open(self.name+".json", 'r') as f:
            self.config = json.load(f)

    def save(self):
        with open(self.name+".json", 'w') as f:
            json.dump(self.config, f)

    def load_defaults(self):
        self.set({"theme": "default", "db": "pages.db", "secret-key": b64encode(os.urandom(24)).decode('utf-8')})
