import sys
from time import sleep


def typewrite(words, space_time, wait_time):
    """
    Prints text out to the screen character by character
    :param words: string to be printed
    :param space_time time interval between each character print
    :param wait_time time after completion of printing and next code
    """
    for char in words:
        sleep(space_time)
        sys.stdout.write(char)
        sys.stdout.flush()
    sleep(wait_time)


def logo_animation(art, line_time, wait_time):
    """
    Prints multi-line text out to the screen line by line
    :param art: large multi-line string to be printed
    :param line_time time interval between each line print
    :param wait_time time after completion of printing and next code
    """
    for line in art.splitlines():
        sleep(line_time)
        print(line)
    sleep(wait_time)


def intro():
    """
    Intro "animation" to be played when the shell launches
    """
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
                """, 0.03, 0.01)
    typewrite('Welcome! Type "?" or "help" to list commands.\n', 0.02, 0.01)
