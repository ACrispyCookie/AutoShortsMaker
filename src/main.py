import json
import os
import sys
from typing import Any, Dict, TextIO

from content.Content import ContentType
import tools.tts.ElevenLabsTTS as ElTTS
from content.types.reddit_ask.RedditAskContent import RedditAskContent

def main():
    print("Starting shorts maker...")
    config: Dict[str, Any] = get_config("data/config.json")
    create_data_file(config["data_path"])

    data: Dict[str, Any] = get_config(config["data_path"])
    secrets: Dict[str, Any] = get_config(config["secrets_path"])
    distribute_secrets(secrets)
    try:
        choice: ContentType = ContentType[sys.argv[1]]
        print("Mode: " + choice.name)
        print("Starting process of creating " + choice.name + " video...")
        if choice == ContentType.REDDIT_ASK:
            RedditAskContent(config, data, secrets).create()
        elif choice == ContentType.OTHER:
            print("wth?")
    except KeyError:
        enum_values: str = ", ".join([content_type.name for content_type in ContentType])
        print(f"Usage: python main.py [{enum_values}]")
    print("Video creation complete!")


def create_data_file(file_path: str):
    if not os.path.exists(file_path):
        f: TextIO = open(file_path, 'w')
        enum_dict: Dict[str, Any] = {content_type.name: {} for content_type in ContentType}
        f.write(json.dumps(enum_dict))


def get_config(file: str) -> Dict[str, Any]:
    with open(file, "r") as f:
        config = json.load(f)
        return config

def distribute_secrets(secrets: Dict[str, Any]):
    ElTTS.set_key(secrets["ELEVEN_LABS"]["api_key"])

if __name__ == '__main__':
    main()
