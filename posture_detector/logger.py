from os import system, name
from threading import Lock
from termcolor import colored
import time
import winsound

class Logger:
    """
    A simpler logger class.
    """

    def __init__(self, logger_name: str):
        self.name = logger_name
        self.lock = Lock()

    def notify(self, message: str, color: str = 'white', with_sound: bool = False):
        """
        Logs a message to the console after obtaining a lock.
        :param color: The color of the message.
        :param with_sound: Whether to play a sound.
        :param message: The message to log.
        """
        self.lock.acquire()
        print(colored(f'[{time.strftime("%H:%M:%S", time.localtime())}] {message}', color))
        self.lock.release()

        if with_sound:
            winsound.Beep(1000, 500)

    def clear_console():
        system('cls')

