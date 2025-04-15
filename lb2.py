from __future__ import annotations

import string
import time
from functools import wraps
from typing import Callable


class Task1CaesarCipher:
    ALPHABET = string.printable

    class CaesarCipherIterator:
        def __init__(self, cipher: Task1CaesarCipher):
            self.cipher = cipher
            self.position = 0

        def __next__(self):
            if self.position >= len(self.cipher.text):
                raise StopIteration

            char = self.cipher.text[self.position]
            self.position += 1

            try:
                char_index = self.cipher.ALPHABET.index(char)
            except ValueError:
                return char

            new_index = char_index - self.cipher.offset if self.cipher.decrypt else char_index + self.cipher.offset

            return self.cipher.ALPHABET[new_index % len(self.cipher.ALPHABET)]

    def __init__(self, text: str, offset: int = 13, decrypt: bool = False) -> None:
        self.text = text
        self.offset = offset
        self.decrypt = decrypt

    def __iter__(self) -> CaesarCipherIterator:
        return self.CaesarCipherIterator(self)


def task1_iterator1() -> None:
    """ Iterator that encrypts ot decrypts text with caesar cipher """

    text = "test тест"
    print(f"Text: {text!r}")

    encrypted = ""
    for char in Task1CaesarCipher(text):
        encrypted += char

    print(f"Encrypted: {encrypted!r}")

    decrypted = ""
    for char in Task1CaesarCipher(encrypted, decrypt=True):
        decrypted += char

    print(f"Decrypted: {decrypted!r}")


def task2_iterator2() -> None:
    ...  # TODO: iterator task


def task3_generator1() -> None:
    ...  # TODO: generator task


def task4_generator2() -> None:
    ...  # TODO: generator task


def task5_dec(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        stop_time = time.time()
        print(f"{func.__name__} took {stop_time - start_time:.2f} seconds to execute")

        return result

    return wrapper


@task5_dec
def task5_func() -> int:
    time.sleep(5)
    return 123


def task5_decorator1() -> None:
    """ Decorator that measures execution time of a function """
    print(f"Executing {task5_func.__name__}...")
    print(f"Result: {task5_func()}")


def task6_dec(cls: type) -> type:
    real_getattr = cls.__getattribute__
    real_setattr = cls.__setattr__

    def new_getattr(self, name: str) -> ...:
        print(f"Getting attribute {name}")
        return real_getattr(self, name)

    def new_setattr(self, name: str, value: ...) -> ...:
        print(f"Setting attribute {name} to {value}")
        return real_setattr(self, name, value)

    cls.__getattribute__ = new_getattr
    cls.__setattr__ = new_setattr

    return cls


@task6_dec
class Task6Class:
    def __init__(self) -> None:
        self.a = 123
        self.b = 456
        self.c = "test"


def task6_decorator2() -> None:
    """ Class decorator that prints all attribute accesses"""
    obj = Task6Class()
    print(f"{obj.a = }")
    obj.b = 789
    print(f"{obj.b = }")
    print(f"{obj.c = }")


def task7_classes1() -> None:
    ...  # TODO: classes task


def task8_classes2() -> None:
    ...  # TODO: classes task


def task9_regex1() -> None:
    ...  # TODO: iterator task


def task10_regex2() -> None:
    ...  # TODO: regex task


def main() -> None:
    tasks = [
        task1_iterator1,
        task2_iterator2,
        task3_generator1,
        task4_generator2,
        task5_decorator1,
        task6_decorator2,
        task7_classes1,
        task8_classes2,
        task9_regex1,
        task10_regex2,
    ]

    for task_func in tasks:
        func_name = task_func.__name__
        print(f"Task #{func_name.split('_')[0][4:]} ({func_name.split('_', 1)[1]})")
        task_func()
        print()


if __name__ == "__main__":
    main()
