import json
import os
import sys
from src.content.JASContent import JASContent
from src.content.RedditAskContent import RedditAskContent


def main():
    print("Clearing data...")
    clearData()
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


def clearData():
    with open("./data/data.json", "w") as f:
        json.dump({"REDDIT_ASK": {"posts": []}, "JAS": {}}, f, indent=4)

    for file in os.listdir("tts/reddit_ask"):
        os.remove("tts/reddit_ask/" + file)
    for file in os.listdir("screenshots/reddit_ask"):
        os.remove("screenshots/reddit_ask/" + file)


def getConfig(file):
    with open("./data/" + file, "r") as f:
        config = json.load(f)
        return config


if __name__ == '__main__':
    main()
