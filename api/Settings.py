
class Settings:
    def __init__(self) -> None:
        self.mongo_uri = "mongodb+srv://chuongpqvn:YIxK7JNeOdB2TvHz@hack-omania.igeosd7.mongodb.net/?retryWrites=true&w=majority&appName=hack-omania"
        self.open_aiKey = "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"
    
    @property
    def mongo_uri(self):
        return self.mongo_uri
    @property
    def open_aiKey(self):
        return self.open_aiKey