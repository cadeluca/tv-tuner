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


def intro():
    logo_animation("""  
            \\  /
         ____\\/_________     88888888888 888     888     88888888888 888     888 888b    888 8888888888 8888888b.  
        |,----------.  |\\        888     888     888         888     888     888 8888b   888 888        888   Y88b 
        ||           |=| |       888     888     888         888     888     888 88888b  888 888        888    888 
        ||          || | |       888     Y88b   d88P         888     888     888 888Y88b 888 8888888    888   d88P 
        ||       . _o| | | __    888      Y88b d88P          888     888     888 888 Y88b888 888        8888888P"  
        |`-----------' |/ /~/    888       Y88o88P  888888   888     888     888 888  Y88888 888        888 T88b   
         ~~~~~~~~~~~~~~~ / /     888        Y888P            888     Y88b. .d88P 888   Y8888 888        888  T88b  
                         ~~      888         Y8P             888      "Y88888P"  888    Y888 8888888888 888   T88b 
         """, 0.03, 0)
    typewrite('Welcome! Type "?" or "help" to list commands.\n', 0.03, 0)
