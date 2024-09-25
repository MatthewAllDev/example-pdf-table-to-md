from pandas import DataFrame
from multiprocessing import Pool, Manager, Queue, Value
from multiprocessing.sharedctypes import Synchronized
from subprocess import CalledProcessError
from typing import Union, List, Dict, Iterable, Any

from tabula import read_pdf

from .constants_and_types import Path, PathLike, TranslateTypes, COUNT_READERS_PROCESS, COUNT_TRANSLATE_PROCESS, COUNT_WRITE_PROCESS
from .item import Item
from .category import Category
from .translators import TranslatorType, LangDetector
from .utils import set_custom_std, reset_std, get_translator
from .progress_bar import ProgressBar


class Reformater:
    def __init__(self, description_lang: str = None):
        manager = Manager()
        self.q_for_read: Queue = manager.Queue()
        self.q_for_translate: Queue = manager.Queue()
        self.q_for_categorization: Queue = manager.Queue()
        self.progres_reading: Synchronized = manager.Value('i', 0)
        self.progres_tranlsating: Synchronized = manager.Value('i', 0)
        self.progres_writing: Synchronized = manager.Value('i', 0)
        self.translator: TranslatorType = get_translator(TranslateTypes.libre, 'auto', description_lang) if description_lang is not None else None

    @classmethod
    def reformat(cls, file_path: PathLike, pages: Union[str, int] = 'all', output_dir_path: PathLike = '', description_lang: str = None) -> None:
        def error_callback(e: Exception) -> None:
            raise e
        item: 'Reformater' = cls(description_lang)
        pages_count: int = item.fill_q_for_read(file_path, pages)
        reader_pool = Pool(COUNT_READERS_PROCESS)
        translate_pool = Pool(COUNT_TRANSLATE_PROCESS)
        results: list = [reader_pool.apply_async(Reformater.start_reading, 
                                                      args=(item.q_for_read, item.q_for_translate, item.progres_reading), 
                                                      error_callback = error_callback) 
                              for _ in range(COUNT_READERS_PROCESS)]
        for _ in range(COUNT_TRANSLATE_PROCESS):
            translate_pool.apply_async(Reformater.start_translating, 
                                       args=(item.q_for_translate, item.q_for_categorization, item.translator, item.progres_tranlsating), 
                                       error_callback = error_callback)
        pb: ProgressBar = ProgressBar('Reading progress', item.progres_reading, pages_count)
        reader_pool.close()
        reader_pool.join()
        pb.stop()
        count_readed_items = sum(result.get() for result in results)
        for _ in range(COUNT_TRANSLATE_PROCESS):
            item.q_for_translate.put('STOP')
        pb: ProgressBar = ProgressBar('Translating progress', item.progres_tranlsating, count_readed_items)
        translate_pool.close()
        translate_pool.join()
        pb.stop()
        categories = item.start_categorization(item.q_for_categorization)
        print(f'{len(categories)} categories read')
        write_pool = Pool(COUNT_WRITE_PROCESS)
        for category in categories.values():
            write_pool.apply_async(item.start_writing, (category, output_dir_path, item.progres_writing))
        pb: ProgressBar = ProgressBar('Writing progress', item.progres_writing, len(categories))
        write_pool.close()
        write_pool.join()
        pb.stop()

    def fill_q_for_read(self, file_path: PathLike, pages: Union[str, int, Iterable]) -> int:
        pages_count: int = 0
        if type(pages) == str:
            if pages == 'all':
                iterator = range(1, 1000)
            elif '-' in pages:
                start, end = pages.split('-')
                iterator = range(int(start), int(end) + 1)
            elif ',' in pages:
                iterator = [int(page) for page in pages.split(',')]
            else:
                raise ValueError(f'Unknown pages type: {type(pages)}')
        elif type(pages) == int:
            iterator = [pages]
        elif type(pages) == Iterable:
            iterator = pages
        else:
            raise ValueError(f'Unknown pages type: {type(pages)}')
        for page in iterator:
            self.q_for_read.put((file_path, page))
            pages_count += 1
        for _ in range(COUNT_READERS_PROCESS):
            self.q_for_read.put(('STOP', None))
        return pages_count

    @staticmethod
    def start_reading(q_input: Queue, q_output: Queue, progress: Synchronized) -> int:
        def to_str(val):
            val = str(val)
            if val == "nan":
                return ""
            return val

        def get_clear_row():
            row = []
            for i in range(8):
                row.append("")
            return row
        
        items_counter: int = 0
        while True:
            file_path, page = q_input.get()
            if file_path == 'STOP':
                break
            set_custom_std()
            try:
                df: (List[DataFrame] | Dict[str, Any]) = read_pdf(file_path, pages = page)
            except CalledProcessError as e:
                if 'Page number does not exist' in e.stderr.decode():
                    reset_std()
                    break
                else:
                    reset_std()
                    raise e
            except Exception as e:
                reset_std()
                raise e
            reset_std()
            for segment in df:
                base_row = get_clear_row()
                for row in segment.values:
                    for i, v in enumerate(row):
                        base_row[i] += to_str(v)
                    if base_row[0] == "":
                        continue
                    item = Item(*base_row[:4], base_row[4:])
                    q_output.put(item)
                    items_counter += 1
                    base_row = get_clear_row()
            progress.value += 1
        return items_counter

    @staticmethod
    def start_translating(q_input: Queue, q_output: Queue, translator: TranslatorType, progress: Synchronized) -> None:
        while True:
            item = q_input.get()
            if item == 'STOP':
                q_output.put('STOP')
                break
            item: 'Item'
            if translator is not None and item.descr:
                item.descr = translator.translate(item.descr)
            q_output.put(item)
            progress.value += 1

    @staticmethod
    def start_categorization(q_input: Queue) -> Dict[str, Category]:
        categories: Dict[str, Category] = {}
        while True:
            item = q_input.get()
            if item == 'STOP':
                break
            item: 'Item'
            category_name: str = item.get_main_category()
            if category_name not in categories:
                categories[category_name] = Category(category_name)
            categories[category_name].append(item)
        return categories

    @staticmethod
    def start_writing(category: Category, output_dir_path: PathLike, progress: Synchronized) -> None:        
        output_dir_path = Path(output_dir_path, 'tables')
        output_dir_path.mkdir(parents = True, exist_ok=True)
        category.to_file(output_dir_path, True)
        progress.value += 1
