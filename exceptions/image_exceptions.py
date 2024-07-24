class ImageTypeNotSupportedError(Exception):
    def __init__(self, message="Image type not supported"):
        self.message = message
        super().__init__(self.message)
