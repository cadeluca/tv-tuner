import linecache
import sqlite3
from cmd import Cmd
from sqlite3 import Error
from click._compat import raw_input
import cli_animations

# Debug variable
debug = True


# TODO: ask Hibbeler if citations are necessary from SQLite official tutorial


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None


def show_tables():
    print("In database named %s, you have the following tables:" % database_name.rstrip('.db'))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in cur.fetchall():
        print("\t" + table[0])
    conn.commit()


def show_schema():
    print("Displaying database schema:\n")
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in cur.fetchall():
        print("Table Name: " + str(table[0]))
        for row in cur.execute("PRAGMA table_info(%s)" % table).fetchall():
            print(row)
        print("\n")
    conn.commit()


def show_table_layout(inp):
    table_list = []
    cur = conn.cursor()
    # should try surrounding this in a try block and doing %s with the table name and just boot out on exception
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in cur.fetchall():
        table_list.append(table[0])
    if inp in table_list:
        headers = []
        cur.execute("PRAGMA table_info(%s)" % inp)
        for i in cur.fetchall():
            headers.append(i[1])
      ##
      ## TODO: formatting output
      ##
        print(headers)
        cur.execute("SELECT * FROM %s" % inp)
        for j in cur.fetchall():
            print(j)

    else:
        print("lol no")
    conn.commit()


# def multi_param(inp):
#     if inp == 'first option':
#
#     elif inp == 'second option':
#         #
#     else:
#         print("Unrecognized or missing parameters. Usage:"
#               "\n\t- show \"table_name\" to display that table.")


def simple_column_select(query_list):
    table = query_list[0]
    column = query_list[1]
    cur = conn.cursor()
    cur.execute('SELECT %s FROM %s' % (column, table))
    result = cur.fetchall()
    for results in result:
        print(results[0])

    # save (commit) the changes
    conn.commit()


def intro():
    cli_animations.logo_animation("""  
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
    cli_animations.typewrite('Welcome! Type "?" or "help" to list commands.\n', 0.03, 0)


class MainPrompt(Cmd):
    prompt = '<tvTuner>'

    def do_exit(self, inp):
        print("Bye")
        return True

    def do_greet(self, inp):
        # typewrite("Welcome to tvTuner!", 0.04, 1)
        print('Hi!')

    def help_greet(self):
        print('the console says hello!')

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def do_tables(self, inp):
        show_tables()

    def do_schema(self, inp):
        show_schema()

    def do_spin(self, inp):
        cli_animations.spin_animation()

    def do_display(self, inp):
        show_table_layout(inp)

    def do_hello(self, s):
        if s == '':
            s = raw_input('Your name please: ')
        print('Hello', s)

    def do_get_column(self, inp):
        params = inp.split()
        if len(params) != 2:
            print("*** invalid number of arguments")
            return
        else:
            simple_column_select(params)

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
        print("Unrecognized command: {}".format(inp))

    # example of multi params in just the command
    def do_add(self, s):
        l = s.split()
        if len(l) != 2:
            print("*** invalid number of arguments")
            return
        try:
            l = [int(i) for i in l]
        except ValueError:
            print("*** arguments should be numbers")
            return
        print(l[0] + l[1])


if __name__ == '__main__':
    path = linecache.getline('db_path.config', 2).rstrip("\n")
    print(path)
    database_name = "sample.db"
    # create a database connection
    conn = create_connection(path + database_name)
    with conn:
        if debug:
            print("connected!")
        MainPrompt().cmdloop(intro())
