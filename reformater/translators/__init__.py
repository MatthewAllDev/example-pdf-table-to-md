from typing import Union

from .argos_translator import Translator as ArgosTranslator
from .google_translator import Translator as GoogleTranslator
from .libre_translator import Translator as LibreTranslator
from .lang_detector import LangDetector


TranslatorType = Union[ArgosTranslator, GoogleTranslator, LibreTranslator]
