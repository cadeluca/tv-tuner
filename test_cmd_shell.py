import sqlite3
from cmd import Cmd
from sqlite3 import Error
import cli_animations

# Debug variable
debug = True


#
# Helper functions
#
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


def find_matching_show(searched_string):
    # do some regex here
    results = []
    return results


#
# SQL style functions
#
def list_tables():
    """ queries database for all tables and
        displays the table names in a column
    """
    print("In database named %s, you have the following tables:" % database_name.rstrip('.db'))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in cur.fetchall():
        print("\t" + table[0])
    conn.commit()


def show_schema():
    """ queries database for the full schema and
        displays the column information per table
    """
    print("Displaying database schema:\n")
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in cur.fetchall():
        print("Table Name: " + str(table[0]))
        for row in cur.execute("PRAGMA table_info(%s)" % table).fetchall():
            print(row)
        print("\n")
    conn.commit()


def list_table_content(inp):
    """ queries database for a matching table to inp
        then displays the table headers and content
    :param inp: user inputted argument
    """
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

        # TODO: format output

        print(headers)
        cur.execute("SELECT * FROM %s" % inp)
        for j in cur.fetchall():
            print(j)

    else:
        print("No matching table '%s'" % inp)

    conn.commit()


def list_columns(desired_table_name):
    """ queries database for a matching table and displays
        the columns that are a part of that table if it exists
    :param desired_table_name desired table to fetch columns for
    """
    cur = conn.cursor()
    desired_table = cur.execute('PRAGMA table_info(%s)' % desired_table_name).fetchall()
    print(desired_table)
    if len(desired_table) != 0:
        print("The table '%s' has the following columns:" % desired_table_name)
        for column in desired_table:
            print("\t" + column[1])
    else:
        print("The table '%s' is not in the database." % desired_table_name)

    conn.commit()


def full_column_return(query_list):
    """ queries database for a matching table and column
        then displays the requested column from the table
    :param query_list list containing column and table
    """
    table = query_list[0]
    column = query_list[1]
    cur = conn.cursor()
    try:
        cur.execute('SELECT %s FROM %s' % (column, table))
        result = cur.fetchall()
        for results in result:
            print(results[0])
    except sqlite3.OperationalError as err:
        print(err)

    conn.commit()


#
# End SQL style functions
#

#
# Simple grammar functions
#

# the following functions will be given a list of possible matching shows from prompt

def detail_viewer(detail_type, show_list):
    cur = conn.cursor()
    if detail_type == 'details':
        # give all information on that show
        # this could be a good spot for a join
        cur.execute("......................................")
    else:
        grammar_dict = {"runtime": "corresponding runtime id", "genre": "", "network": "", "seasons": "", "status": ""}
        detail = grammar_dict[detail_type]
        table = "" # this should be the table we get this info from
        if len(show_list) == 1:
            # show detail is
            # do sql
            print("")
        else:
            for show in show_list:
                # select <runtime> from <table that has runtime> where <name id> = <name>
                result = cur.execute("SELECT %s FROM %s WHERE nameidtobechanged = '%s'" % (detail, table, show)).fetchone()

#
# End Simple grammar functions
#


#
# Complex grammar functions
#

# TODO @cadeluca: complete this @ other todo
def show_finder(search_request_list):
    print(search_request_list)
    # request_list reads like:   look for a show

#
# End Complex grammar functions
#



class MainPrompt(Cmd):
    prompt = '<tvTuner> '

    def do_exit(self, inp):
        cli_animations.typewrite("Tune in next time!", 0.04, 0.04)
        return True

    def help_exit(self):
        print('Exits the application. Shorthand: `x` `q` `Ctrl-D`.')

    def do_tables(self, inp):
        list_tables()

    def do_schema(self, inp):
        show_schema()

    def do_list(self, inp):
        list_table_content(inp)

    def do_runtime(self, inp):
        # do regex search for shows, return a list
        show_list = find_matching_show(inp)
        detail_viewer('runtime', show_list)

    def do_get_column(self, inp):
        params = inp.split()
        if len(params) == 2:
            full_column_return(params)
        elif len(params) == 1:
            list_columns(params[0])
        else:
            print("Invalid number of arguments.\nUsage:"
                  "\n\tget_column 'table' - returns a list of columns in that table."
                  "\n\tget_column 'table' 'column' - returns the contents of that column from that table.")
            return

    # TODO: ASK HIBBELER IF THIS COUNTS AS USING THE GRAMMAR
    # TODO @cadeluca: continue to work on this
    def do_find(self, inp):
        if inp == '':
            print("What do you want to find? Enter the first character or the word to search:")
            print("\t[1] tracks\t[2] albums\n\t[3] artists\t[4] genres\n\t[5] cancel")
            valid_search = False
            search_request = []
            valid_options = ['1', '2', '3', '4', '5', 'tracks', 'albums', 'artists', 'genres', 'cancel']
            while not valid_search:
                try:
                    search_type = input('- find: ')
                except ValueError:
                    print("that is not one of the options")
                    continue
                if search_type not in valid_options:
                    print("that is not one of the options")
                    continue
                else:
                    valid_search = True
            print("woo! here we would link to the valid search for each type, by calling the appropriate function")

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
        print("Unrecognized command: {}".format(inp))


if __name__ == '__main__':
    # TODO: replace this with our database once we have it
    database_name = "sample.db"
    # create a database connection
    conn = create_connection('db/' + database_name)
    with conn:
        if debug:
            print("connected!")
        MainPrompt().cmdloop(cli_animations.intro())

