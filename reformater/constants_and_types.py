from typing import Union
from pathlib import Path
from dataclasses import dataclass

PRICE_WEIGHTS = {'Платная': 2, 'Условно бесплатная': 1, 'Бесплатная': 0, '': 0}
PathLike = Union[str, Path]
COUNT_READERS_PROCESS = 2
COUNT_TRANSLATE_PROCESS = 2
COUNT_WRITE_PROCESS = 4

@dataclass
class TranslateTypes:
    google: str = 'google'
    argos: str = 'argos'
    libre: str = 'libre'
