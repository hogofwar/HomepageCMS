import os, json
from base64 import b64encode

class Config:
    config = {}

    def get(self, key):
        return self.config[key]

    def set(self, key, value, save=False):
        self.config[key] = value
        if save:
            self.save()

    def load(self, file = "config.json"):
        if not os.path.isfile(file):
            self.load_defaults()
            self.save(file)

        with open(file, 'r') as f:
            self.config = json.load(f)

    def save(self, file = "config.json"):
        with open(file, 'w') as f:
            json.dump(self.config, f)

    def load_defaults(self):
        self.config={
            "theme": "default",
            "db": "pages.db",
            "secret-key": b64encode(os.urandom(24)).decode('utf-8')}
