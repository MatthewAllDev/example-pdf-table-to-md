from .constants_and_types import TranslateTypes
from .translators import LibreTranslator, ArgosTranslator, GoogleTranslator, TranslatorType


def get_translator(translator_type: str, from_code: str, to_code: str) -> TranslatorType:
    if translator_type == TranslateTypes.libre:
        Tanslator = LibreTranslator('http://localhost:5000', to_code, from_code)
    if translator_type == TranslateTypes.argos:
        Tanslator = ArgosTranslator(from_code, to_code)
    elif translator_type == TranslateTypes.google:
        Tanslator = GoogleTranslator(from_code, to_code)
    else:
        raise ValueError(f'Unknown translator type: {translator_type}')
    return Tanslator

