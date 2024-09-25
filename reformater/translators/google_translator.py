from googletrans import Translator as GTranslator
from httpx import Timeout

class Translator(GTranslator):
    def __init__(self, from_code: str, to_code: str):
        self.from_code: str = from_code
        self.to_code: str = to_code
        super().__init__(timeout=Timeout(30))

    def translate(self, text):
        return super().translate(text, self.to_code, self.from_code).text

    def __str__(self) -> str:
        return f'Translator({self.from_code}-{self.to_code})'