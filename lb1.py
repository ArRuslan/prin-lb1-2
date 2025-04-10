import math
import os
import random
from typing import Literal


def task1_if_else() -> None:
    """ Check if last two digits of a number is divisible by 3 and 5 or 5 and 7 """
    number = 123
    last_digits = number % 100

    if last_digits % 5 != 0:
        print("Not divisible by 3 and 5 or 5 and 7")
    elif last_digits % 3 == 0:
        print("Divisible by 3 and 5")
    elif last_digits % 7 == 0:
        print("Divisible by 5 and 7")


def task2_loop() -> None:
    """ N-th fibonacci number contains 3 """
    N = 50

    a = 0
    b = 1
    for _ in range(N):
        a, b = b, a + b

    print(f"{N}-th fibonacci number is {b}")

    while b > 0:
        if b % 10 == 3:
            print(f"{N}-th fibonacci number contains 3")
            return
        b //= 10

    print(f"{N}-th fibonacci number does not contain 3")


def task3_calc(a: float | None = None, b: float | None = None, op: Literal["+", "-", "*", "/"] | None = None) -> None:
    a = a if a is not None else float(input("First number: "))
    b = b if b is not None else float(input("Second number: "))
    op = op or input("Operation (+, -, /, *): ")

    if op not in ("+", "-", "/", "*"):
        print("Invalid operation!")
        return

    result = None
    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    elif op == "/":
        result = a / b

    print(f"Result of {a} {op} {b}: {result}")


def task3_input_output() -> None:
    """ Simple calculator """
    task3_calc()


def task4_tuples_dicts() -> None:
    """ Count all character pairs in text """
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis et ornare mi, at convallis massa. Nulla iaculis massa dui, nec vestibulum lacus porta vitae. Fusce et maximus orci. Curabitur ut tellus cursus, tempus nisl vitae, maximus magna. Morbi vel justo."
    counts = {}

    print(f"Text: {text}")

    for i in range(len(text) - 1):
        pair = text[i], text[i + 1]
        if pair not in counts:
            counts[pair] = 0
        counts[pair] += 1

    print("Pair counts (first 5):")
    for idx, (pair, count) in enumerate(counts.items()):
        if idx >= 5:
            break
        print(f"  {pair} - {count}")

    print("5 most common pairs:")
    for pair, count in sorted(list(counts.items()), key=lambda it: it[1], reverse=True)[:5]:
        print(f"  {pair} - {count}")


def task5_lists() -> None:
    """ Create 8x8 matrix from random list of 64 elements and reverse it """
    lst = [random.randint(0, 32) for _ in range(64)]
    mat_size = int(math.sqrt(len(lst)))

    print(f"List: {lst}")

    mat = []
    for row in range(mat_size):
        mat.append(lst[row * mat_size:(row + 1) * mat_size])

    print("Matrix: ")
    for row in mat:
        for col in row:
            print(f"{col:<3}", end="")
        print()

    for row in mat:
        row.reverse()
    mat.reverse()

    print("Matrix: ")
    for row in mat:
        for col in row:
            print(f"{col:<3}", end="")
        print()


def task6_strings() -> None:
    """ Find longest common prefix amongst a list if strings """
    strings = ["asdqwe", "asdasd", "as123"]
    prefix = ""
    for char in strings[0]:
        for st in strings[1:]:
            if not st.startswith(f"{prefix}{char}"):
                print(f"Longest common prefix is {prefix!r}")
                return
        prefix += char

    print(f"Longest common prefix is {prefix!r}")


def task7_functions() -> None:
    """ Call calculator function from task 3 with predefined numbers a and b and operation """
    a, b, op = 15, 85, "*"
    print(f"Calling calc function with {a=}, {b=}, {op=!r}")
    task3_calc(a, b, op)

    a, b, op = 840, 42, "/"
    print(f"Calling calc function with {a=}, {b=}, {op=!r} as kwargs")
    task3_calc(a=a, b=b, op=op)


def task8_lambdas() -> None:
    """ Sort random list of tuples using lambda for key """
    lst = [
        (random.randint(-32, 32), random.randint(-32, 32))
        for _ in range(32)
    ]
    print(f"Before sorting: {lst}")

    lst.sort(key=lambda e: e[0])
    print(f"After sorting by first tuple number: {lst}")

    lst.sort(key=lambda e: e[1])
    print(f"After sorting by second tuple number: {lst}")

    lst.sort(key=lambda e: abs(e[1] - e[0]))
    print(f"After sorting by difference between first and second tuple numbers: {lst}")


class CalcException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


def _task9_invalid_number() -> None:
    a, b, op = "asd", 85, "+"
    try:
        task3_calc(a, b, op)
    except (ValueError, TypeError) as e:
        raise CalcException(f"Call to calc function with {a=}, {b=}, {op=} raised an exception: {e}")


def _task9_zero_division() -> None:
    a, b, op = 42, 0, "/"
    try:
        task3_calc(a, b, op)
    except ZeroDivisionError as e:
        raise CalcException(f"Call to calc function with {a=}, {b=}, {op=} raised an exception: {e}")


def _task9_no_error() -> None:
    a, b, op = 42, 0, "*"
    task3_calc(a, b, op)


def task9_exceptions() -> None:
    """ Intercept exceptions from task 3 calc function about invalid numbers and zero division and raise new exception """
    for func in (_task9_invalid_number, _task9_zero_division, _task9_no_error):
        try:
            func()
        except CalcException as e:
            print(f"{func.__name__}: {e.__class__.__name__}: {e.message}")
        else:
            print(f"{func.__name__} did not raise an exception")


def task10_fs() -> None:
    """ Read first line (or first 16 bytes if file is binary) from every file in current directory """

    for file_name in os.listdir():
        if not os.path.isfile(file_name):
            print(f"{file_name} is not a file, skipping")
            continue

        with open(file_name, "rb") as f:
            line = f.readline()
            try:
                line = line.decode("utf8")
            except UnicodeDecodeError:
                f.seek(0)
                line = f.read(16).hex()

            print(f"{file_name}: {line!r}")


def main() -> None:
    tasks = [
        task1_if_else,
        task2_loop,
        task3_input_output,
        task4_tuples_dicts,
        task5_lists,
        task6_strings,
        task7_functions,
        task8_lambdas,
        task9_exceptions,
        task10_fs,
    ]

    for task_func in tasks:
        func_name = task_func.__name__
        print(f"Task #{func_name.split('_')[0][4:]} ({func_name.split('_', 1)[1]})")
        task_func()
        print()


if __name__ == "__main__":
    main()
