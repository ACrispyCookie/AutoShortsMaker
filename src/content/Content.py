import json
import os
from enum import Enum
from typing import Dict, Any


class ContentType(Enum):
    REDDIT_ASK = 1
    OTHER = 2


class Content:
    def __init__(self, content_type: ContentType, config: Dict[str, Any], data: Dict[str, Any], secrets: Dict[str, Any]):
        self.type: ContentType = content_type
        self.config: Dict[str, Any] = config[content_type.name]
        self.data: Dict[str, Any] = data[content_type.name]
        self.secrets: Dict[str, Any] = secrets[content_type.name]
        self.dirs: Dict[str, Any] = config[content_type.name]['dirs']
        self.config_json: Dict[str, Any] = config
        self.data_json: Dict[str, Any] = data

        self.create_dirs()

    def create_dirs(self):
        for folder_type in self.dirs:
            if not os.path.exists(self.dirs[folder_type]):
                os.makedirs(self.dirs[folder_type])

    def create(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def save_data(self):
        self.data_json[self.type.name] = self.data
        with open(self.config_json["data_path"], "w") as f:
            json.dump(self.data_json, f, indent=4)
