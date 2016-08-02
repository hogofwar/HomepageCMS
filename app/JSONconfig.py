import os, json


class Config:

    def __init__(self, name):
        self.name = name
        self.config = {}
        self.load()

    def get(self, key, default = None):
        value = self.config.get(key)
        if value is None:
            self.set({key: default})
            return default
        return value

    def set(self, pairs, save=True):
        self.config.update(pairs)
        if save:
            self.save()

    def load(self):
        if not os.path.isfile(self.name+".json"):
            self.save()
        else:
            with open(self.name+".json", 'r') as f:
                self.config = json.load(f)

    def save(self):
        with open(self.name+".json", 'w') as f:
            json.dump(self.config, f)
