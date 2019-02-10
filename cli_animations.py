import sys
from time import sleep


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


def spin_animation():
    spinner = spinning_cursor()
    for _ in range(50):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sleep(0.1)
        sys.stdout.write('\b')


def typewrite(words, space_time, wait_time):
    for char in words:
        sleep(space_time)
        sys.stdout.write(char)
        sys.stdout.flush()
    sleep(wait_time)


def logo_animation(art, line_time, wait_time):
    for line in art.splitlines():
        sleep(line_time)
        print(line)
    sleep(wait_time)
