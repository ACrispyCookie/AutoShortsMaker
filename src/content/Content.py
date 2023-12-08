import json


class Content:
    def __init__(self, content_type, config, data):
        self.type = content_type
        self.config = config[content_type]
        self.data = data[content_type]
        self.configJson = config
        self.dataJson = data

    def create(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def saveData(self):
        self.dataJson[self.type] = self.data
        with open("./data/data.json", "w") as f:
            json.dump(self.dataJson, f, indent=4)
