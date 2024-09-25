from pathlib import Path
import re

from fasttext import load_model

from .utils import download_file

class LangDetector:
    def __init__(self):
        model_path = Path(__file__).parent / 'models' / 'lid.176.bin'
        if not model_path.exists():
            print('Downloading language detect model')
            download_file('https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin', model_path)
        self.__model = load_model(str(model_path))

    def detect(self, text):
        return self.__model.predict(text)[0][0].split('__')[-1]
    
    @staticmethod
    def has_cyrillic(text: str) -> bool:
        cyrillic_count = len(re.findall(r'[\u0400-\u04FF]', text))
        total_alpha_count = len(re.findall(r'[a-zA-Z\u0400-\u04FF]', text))
        
        if total_alpha_count == 0:
            return False
        return (cyrillic_count / total_alpha_count) > 0.25
