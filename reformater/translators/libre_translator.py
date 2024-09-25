from requests import post, Response
from typing import Tuple, List, Dict, Union

class Translator:
    def __init__(self, url: str, to_code: str, from_code: str = 'auto', api_key: str = None):
        self.__url: str = url
        self.__headers: Dict[str, str] = { 'Content-Type': 'application/json' }
        self.__body_base: Dict[str, str] = {} if api_key is None else { 'api_key': api_key }
        self.__body_to_translate: Dict[str, str] = {
            'source': from_code,
            'target': to_code
        } | self.__body_base

    def translate(self, text: str, alternatives: int = 1) -> Union[str, List[str]]:
        body: Dict[str, Union[str, int]] = self.__body_to_translate | { 'q': text, 'alternatives': alternatives }
        response: Response = post(f'{self.__url}/translate', headers=self.__headers, json=body)
        response_data: Dict[str, Union[str, int, List, Dict]] = response.json()
        if 'error' in response_data:
            raise RuntimeError(response_data['error'])
        if alternatives > 1:
            return response_data['alternatives'].insert(0, response_data['translatedText'])
        else:
            return response_data['translatedText']
        
    def detect(self, text: str) -> List[Tuple[str, int]]:
        body: Dict[str, Union[str, int]] = self.__body_base | { 'q': text }
        response: Response = post(f'{self.__url}/detect', headers=self.__headers, json=body)
        response_data: Dict[str, Union[str, int, List, Dict]] = response.json()
        return response_data
