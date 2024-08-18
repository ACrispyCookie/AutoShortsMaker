import json
import os
import sys
from typing import Any

from content.Content import ContentType
from content.types.reddit_ask.RedditAskContent import RedditAskContent

def main():
    print("Starting shorts maker...")
    config = get_config("data/config.json")
    create_data_file(config["data_path"])

    data = get_config(config["data_path"])
    try:
        choice: ContentType = ContentType[sys.argv[1]]
        print("Mode: " + choice.name)
        print("Starting process of creating " + choice.name + " video...")
        if choice == ContentType.REDDIT_ASK:
            RedditAskContent(config, data).create()
        elif choice == ContentType.OTHER:
            print("wth?")
    except KeyError:
        enum_values = ", ".join([content_type.name for content_type in ContentType])
        print(f"Usage: python main.py [{enum_values}]")
    print("Video creation complete!")


def create_data_file(file_path: str):
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        enum_dict = {content_type.name: {} for content_type in ContentType}
        f.write(json.dumps(enum_dict))


def get_config(file: str) -> Any:
    with open(file, "r") as f:
        config = json.load(f)
        return config

if __name__ == '__main__':
    main()
