

class TitleAlreadyExists(Exception):
    def __init__(self, title):
        super().__init__(f'Title {title} already exists!')
