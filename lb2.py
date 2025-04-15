from __future__ import annotations

import random
import re
import string
import time
from functools import wraps
from typing import Callable, Generator


class Task1CaesarCipher:
    ALPHABET = string.printable

    __slots__ = ("text", "offset", "decrypt",)

    class CaesarCipherIterator:
        __slots__ = ("cipher", "position",)

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


def task3_fibonacci(n: int) -> Generator[int, None, None]:
    a = 0
    b = 1
    for _ in range(n):
        a, b = b, a + b
        yield b


def task3_generator1() -> None:
    """ Fibonacci generator """

    print("First 10 fibonacci numbers from generator")

    for num in task3_fibonacci(10):
        print(num)


def task4_filter_primes(nums: list[int]) -> Generator[int, None, None]:
    for num in nums:
        if num <= 1 or num % 2 == 0:
            continue
        is_prime = True
        for i in range(3, int(num ** 0.5 + 1), 2):
            if num % i == 0:
                is_prime = False
                break

        if is_prime:
            yield num


def task4_generator2() -> None:
    """ Generator to filter only prime numbers """
    nums = [random.randint(2, 100) for _ in range(32)]
    print(f"Nums: {nums}")

    print("Primes:")
    for prime in task4_filter_primes(nums):
        print(prime)


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
        print(f"Setting attribute {name} to {value!r}")
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
    """ Extract all "a" links from html """
    html = """
<html>
<body>
<div>
    <h1>Example Domain</h1>
    <p>This domain is for use in illustrative examples in documents. You may use this
    domain in literature without prior coordination or asking for permission.</p>
    <p><a a="b" b="c" href="https://www.iana.org/domains/example">More information...</a></p>
</div>
</body>
</html>
"""

    links = re.findall(
        r'<a(?:\s+[a-zA-Z0-9_-]=[\'"].+?[\'"])*?\shref="(https?://(?:[a-zA-Z0-9-]+\.)+?[a-zA-Z0-9-]+\.[a-zA-Z]{2,12}(?:(?:/\S+?)+?))".*?>',
        html
    )

    for link in links:
        print(link)


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
