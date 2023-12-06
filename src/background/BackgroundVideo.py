class BackgroundVideo:

    def __init__(self, folder, name):
        self.folder = folder
        self.name = name

    def download(self):
        raise NotImplementedError("Subclass must implement abstract method")
