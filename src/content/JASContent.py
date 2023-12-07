from src.content.Content import Content


class JASContent(Content):

    def __init__(self, config, data):
        super().__init__("JAS", config, data)

    def create(self):
        print("JASContent.create()")
