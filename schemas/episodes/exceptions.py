class EpisodeAlreadyExists(Exception):
    def __init__(self, message):
        super().__init__(message)


class EpisodeNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
