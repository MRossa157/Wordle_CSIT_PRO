from enum import Enum

MAX_WORD_LENGTH = 5
MAX_ATTEMPT_NUMBER = 6


class GameStatus(Enum):
    WIN: str = 'WIN'
    IN_PROGRESS: str = 'IN_PROGRESS'
    LOSS: str = 'LOSS'


class WordTypes(Enum):
    CORRECT: str = 'GREEN'
    WRONG_PLACE: str = 'YELLOW'
    NOT_CORRECT: str = 'BLACK'
