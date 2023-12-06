from src.content.Content import Content


class JASContent(Content):

    def __init__(self):
        super().__init__("JAS")

    def create(self):
        print("JASContent.run()")
