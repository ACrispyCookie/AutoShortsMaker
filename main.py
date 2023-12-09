import json
import os
import sys
from src.content.JASContent import JASContent
from src.content.RedditAskContent import RedditAskContent


def main():
    print("Starting shorts maker...")
    choice = sys.argv[1]
    config = getConfig("data/config.json")
    createDataFile(config["data_path"])

    data = getConfig(config["data_path"])
    if choice == 'REDDIT_ASK':
        print("Mode: RedditAsk")
        print("Starting process of creating RedditAsk video...")
        RedditAskContent(config, data).create()
    elif choice == 'JAS':
        print("Mode: JAS")
        print("Starting process of creating JAS video...")
        JASContent(config, data).create()
    else:
        print("Usage: python main.py [REDDIT_ASK|JAS]")
    print("Video creation complete!")


def createDataFile(file_path):
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write(json.dumps({"REDDIT_ASK": {}, "JAS": {}}))


def getConfig(file):
    with open(file, "r") as f:
        config = json.load(f)
        return config


if __name__ == '__main__':
    main()
