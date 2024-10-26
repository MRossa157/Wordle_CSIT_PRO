from dataclasses import dataclass


@dataclass(init=False, repr=False, eq=False, frozen=True, match_args=False)
class _WordTypes:
    CORRECT: str = 'CORRECT'
    NOT_CORRECT: str = 'NOT_CORRECT'
    WRONG_PLACE: str = 'WRONG_PLACE'


word_types = _WordTypes()
