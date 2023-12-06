import sys
from src.content.JASContent import JASContent
from src.content.RedditAskContent import RedditAskContent


def main():
    choice = sys.argv[1]
    if choice == 'reddit_ask':
        print("Creating RedditAsk content...")
        RedditAskContent().create()
    elif choice == 'jas':
        print("Creating JAS content...")
        JASContent().create()
    else:
        print("Usage: python main.py [reddit_ask|jas]")


if __name__ == '__main__':
    main()
