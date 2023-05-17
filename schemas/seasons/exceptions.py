class SeasonAlreadyExists(Exception):
    def __init__(self, message):
        super().__init__(message)


class SeasonNoOneWatchedEpisode(Exception):
    def __init__(self, message):
        super().__init__(message)


class SeasonNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
