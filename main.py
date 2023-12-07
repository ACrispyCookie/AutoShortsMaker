import json
import sys
from src.content.JASContent import JASContent
from src.content.RedditAskContent import RedditAskContent


def main():
    print("Starting shorts maker...")
    choice = sys.argv[1]
    config = getConfig("config.json")
    data = getConfig("data.json")
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


def getConfig(file):
    with open("./data/" + file, "r") as f:
        config = json.load(f)
        return config


if __name__ == '__main__':
    main()
