from __future__ import annotations

import os
import random
import re
import string
import time
from abc import abstractmethod, ABC
from functools import wraps
from typing import Callable, Generator, Any


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


class Task2FileList:
    __slots__ = ("file_names",)

    class FileLineIterator:
        __slots__ = ("file_list", "position",)

        def __init__(self, file_list: Task2FileList):
            self.file_list = file_list
            self.position = 0

        def __next__(self) -> str | None:
            if self.position >= len(self.file_list.file_names):
                raise StopIteration

            file_name = self.file_list.file_names[self.position]
            self.position += 1

            if not os.path.isfile(file_name):
                return None

            with open(file_name, "rb") as f:
                try:
                    return f.readline().decode("utf8")
                except UnicodeDecodeError:
                    return None

    def __init__(self, file_names: list[str]) -> None:
        self.file_names = file_names

    def __iter__(self) -> FileLineIterator:
        return self.FileLineIterator(self)


def task2_iterator2() -> None:
    """ Iterator to return first line (or None if file is binary) from each file from list """
    file_names = os.listdir()
    for file_name, file_content in zip(file_names, Task2FileList(file_names)):
        print(f"{file_name} - {file_content!r}")


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


class Task7Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...


class Task7Rectagle(Task7Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * self.width + 2 * self.height


class Task7Circle(Task7Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return 3.14 * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * 3.14 * self.radius


def task7_classes1() -> None:
    """ Create abstract shape (base) class with area and perimeter method, create rectangle and circle classes """
    rect1 = Task7Rectagle(2, 3)
    rect2 = Task7Rectagle(3, 4)

    circle1 = Task7Circle(5)
    circle2 = Task7Circle(7)

    print(f"Rectangle(width={rect1.width:.2f}, height={rect1.height:.2f}): area = {rect1.area():.2f}, perimeter = {rect1.perimeter():.2f}")
    print(f"Rectangle(width={rect2.width:.2f}, height={rect2.height:.2f}): area = {rect2.area():.2f}, perimeter = {rect2.perimeter():.2f}")
    print(f"Circle(radius={circle1.radius:.2f}): area = {circle1.area():.2f}, perimeter = {circle1.perimeter():.2f}")
    print(f"Circle(radius={circle2.radius:.2f}): area = {circle2.area():.2f}, perimeter = {circle2.perimeter():.2f}")


class Task8Metaclass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(cls, *args, **kwargs)
        return cls._instances[cls]
    def __new__(cls, name: str, bases: tuple[type], attrs: dict[str, ...]):
        def _get_instance(_cls):
            return _cls()

        attrs["get_instance"] = classmethod(_get_instance)
        return super().__new__(cls, name, bases, attrs)


class Task8Singleton(metaclass=Task8Metaclass):
    def __init__(self, a: int = 1, b: int = 2, c: str = "test") -> None:
        self.a = a
        self.b = b
        self.c = c


def task8_classes2() -> None:
    """ Singleton via metaclass """

    obj1 = Task8Singleton(123)
    print(f"{id(obj1)=}, {obj1.a=}, {obj1.b=}, {obj1.c=}")

    obj2 = Task8Singleton(456, 789, "qwe")
    print(f"{id(obj2)=}, {obj2.a=}, {obj2.b=}, {obj2.c=}")

    obj3 = Task8Singleton.get_instance()
    print(f"{id(obj3)=}, {obj3.a=}, {obj3.b=}, {obj3.c=}")


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
    """ Validate rfc3339 datetime """
    datetime_re = re.compile(r'^((?:(\d{4}-(?:(?:(?:01|03|05|07|08|10|12)-(?:0[1-9]|[12]\d|3[01]))|(?:(?:04|06|09|11)-(?:0[1-9]|[12]\d|30))|(?:(?:02)-(?:0[1-9]|[1]\d|2[0-8]))))T((?:[01]\d|2[0-4]):[0-5]\d:[0-5]\d(?:\.\d+)?))(Z|[\+-]\d{2}:\d{2})?)$')

    to_validate = [
        "2025-01-19T15:21:32.59+02:00",
        "2025-01-19T00:21:32.59+02:00",
        "2025-01-19T23:59:59.99+02:00",
        "2025-01-19T00:00:00+02:00",
        "2025-01-19T00:00:60+02:00",
        "2025-01-19T00:60:00+02:00",
        "2025-01-19T00:98:00+02:00",
        "2025-01-19T25:00:00+02:00",
        "2025-01-32T00:00:00+02:00",
        "2025-00-32T00:00:00+02:00",
        "2025-01-00T00:00:00+02:00",
        "2025-02-29T00:00:00+02:00",
        "2025-13-20T00:00:00+02:00",
        "0000-01-01T00:00:00+02:00",
    ]

    for date in to_validate:
        print(f"Is \"{date}\" valid: {datetime_re.match(date) is not None}")


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
