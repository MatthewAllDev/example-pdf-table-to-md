from sys import stdout
import math
from multiprocessing import Process, Event
from multiprocessing.sharedctypes import Synchronized
from time import sleep


class ProgressBar:
    def __init__(self, title: str, counter, max_count: int):
        self.__title: str = title
        self.__counter: Synchronized = counter
        self.__max_count: int = max_count
        self.__stop_event = Event()
        self.__process: Process = Process(target=self.show, args=(title, counter, max_count, self.__stop_event))
        self.__process.start()

    @staticmethod
    def __show(title: str, counter: Synchronized, max_count: int):
        progress: float = counter.value / max_count
        points_count: int = math.floor(progress * 25)
        stdout.write(
            f"\r{title}: [{'#' * points_count}{'_' * (25 - points_count)}] "
            f"{str(round(progress * 10000) / 100)}%")
        stdout.flush()
         
    @staticmethod
    def show(title: str, counter: Synchronized, max_count: int, stop_event):
        while not stop_event.is_set():
            ProgressBar.__show(title, counter, max_count)
            sleep(1)

    def stop(self):
        self.__counter.value = self.__max_count
        self.__show(self.__title, self.__counter, self.__max_count)
        print()
        # print(self.__counter, self.__max_count)
        self.__stop_event.set()
        self.__process.join()
