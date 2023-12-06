class Content:
    def __init__(self, content_type):
        self.type = content_type

    def create(self):
        raise NotImplementedError("Subclass must implement abstract method")
