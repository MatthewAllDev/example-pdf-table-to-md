from pathlib import Path

import argostranslate.package
import argostranslate.translate

from .utils import download_file

available_packages = argostranslate.package.get_available_packages()

class Translator:
    def __init__(self, from_code: str, to_code: str):
        self.from_code: str = from_code
        self.to_code: str = to_code
        argostranslate.package.update_package_index()
        packages = list(filter(
            lambda x: x.from_code == from_code and x.to_code == to_code,
            available_packages
        ))
        if not packages:
            raise ValueError(f"No translation package available for {from_code} to {to_code}")
        package_to_install = packages[0]
        model_path: Path = self.__download_model(package_to_install)
        print(f'Installing {package_to_install.code} model...')
        argostranslate.package.install_from_path(model_path)

    def __download_model(self, package: argostranslate.package.AvailablePackage) -> Path:
        model_path = Path(Path(__file__).parent, 'models', f'{package.code}.argosmodel')
        model_path.parent.mkdir(parents=True, exist_ok=True)
        if not model_path.exists():
            print(f'Downloading {package.code} model...')
            download_file(
                package.links[0],
                model_path,
                headers={'User-Agent': 'ArgosTranslate'},
            )
        return model_path

    def translate(self, text: str) -> str:
        return argostranslate.translate.translate(text, self.from_code, self.to_code)

    def __str__(self) -> str:
        return f'Translator({self.from_code}-{self.to_code})'