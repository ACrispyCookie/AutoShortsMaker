import json
import os


class Content:
    def __init__(self, content_type, config, data):
        self.type = content_type
        self.config = config[content_type]
        self.data = data[content_type]
        self.dirs = config[content_type]['dirs']
        self.configJson = config
        self.dataJson = data

        self.create_dirs()

    def create_dirs(self):
        for folder_type in self.dirs:
            if not os.path.exists(self.dirs[folder_type]):
                os.makedirs(self.dirs[folder_type])

    def create(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def save_data(self):
        self.dataJson[self.type] = self.data
        with open(self.configJson["data_path"], "w") as f:
            json.dump(self.dataJson, f, indent=4)
