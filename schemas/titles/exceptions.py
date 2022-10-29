class TitleAlreadyExists(Exception):
    def __init__(self, title):
        super().__init__(f'Title {title} already exists!')


class TitleNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)
