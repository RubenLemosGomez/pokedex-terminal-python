import platform
import random
import subprocess


def generate_random_id() -> int:
    return random.randint(1, 1025)


def clean_terminal() -> None:
    sistema = platform.system()

    if sistema == "Windows":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)
