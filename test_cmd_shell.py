from cmd import Cmd

# TODO:
# import sqlite3


class MainPrompt(Cmd):
    prompt = '<$CS205-TV-TUNER> '
    intro = """  
        \\  /
     ____\\/_________     88888888888 888     888     88888888888 888     888 888b    888 8888888888 8888888b.  
    |,----------.  |\\        888     888     888         888     888     888 8888b   888 888        888   Y88b 
    ||           |=| |       888     888     888         888     888     888 88888b  888 888        888    888 
    ||          || | |       888     Y88b   d88P         888     888     888 888Y88b 888 8888888    888   d88P 
    ||       . _o| | | __    888      Y88b d88P          888     888     888 888 Y88b888 888        8888888P"  
    |`-----------' |/ /~/    888       Y88o88P  888888   888     888     888 888  Y88888 888        888 T88b   
     ~~~~~~~~~~~~~~~ / /     888        Y888P            888     Y88b. .d88P 888   Y8888 888        888  T88b  
                     ~~      888         Y8P             888      "Y88888P"  888    Y888 8888888888 888   T88b 
                                                             
Welcome! Type "?" or "help" to list commands\n"""

    def do_exit(self, inp):
        print("Bye")
        return True

    def do_greet(self, inp):
        print('Hi!')

    def help_greet(self):
        print('the console says hello!')

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    # def do_add(self, inp):
    #     print("adding '{}'".format(inp))

    # def help_add(self):
    #     print("Add a new entry to the system.")

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        print("Unrecognized command: {}".format(inp))

    do_EOF = do_exit
    help_EOF = help_exit


if __name__ == '__main__':
    MainPrompt().cmdloop()
