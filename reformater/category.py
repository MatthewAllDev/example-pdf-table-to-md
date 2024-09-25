import re

from .constants_and_types import PathLike, Path
from .item import Item

class Category(list):
    def __init__(self, name: str):
        self.name = name if name[0] != "#" else name[1:]
        super().__init__()

    def append(self, object: 'Item') -> None:
        return super().append(object)

    def to_file(self, dir_path: PathLike = '', rewrite: bool = True) -> str:

        def clean_filename(name: str, default: str = 'default_filename') -> str:
            invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
            cleaned_name = re.sub(invalid_chars, '_', name)
            cleaned_name = cleaned_name.strip()
            if not cleaned_name:
                cleaned_name = default
            return cleaned_name

        self.sort(key=lambda el: el.price_weight)
        file_path: Path = Path(dir_path, f'{clean_filename(self.name)}.md')
        write_head: bool = rewrite or not file_path.exists()
        with open(file_path, 'w' if rewrite else 'a') as f:
            if write_head:
                f.write(f'{self.name}\n\n')
                f.write('| Название | Условия использования | Описание | Категория #1 | Категория #2 | Категория #3 | Категория #4 |\n')
                f.write('| ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |\n')
            for item in self:
                f.write(str(item) + '\n')
