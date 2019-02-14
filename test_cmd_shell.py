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
    except Error as err:
        print(err)
    return None


def find_matching_show(searched_string):
    """ query the database for the all types of matches
        on the searched string and return a list of results
    :param searched_string: string to use in LIKE query
    :return: list of matches
    """
    cur = conn.cursor()
    # TODO: replace title and employees with the corresponding values from new db
    results = cur.execute("SELECT title FROM employees WHERE title LIKE '%"+searched_string+"%';").fetchall()
    results_list = []
    for result in results:
        if debug:
            print(result[0])
        results_list.append(result[0])
    conn.commit()
    return results_list


#
# SQL style functions
#
def list_tables():
    """ queries database for all tables and
        displays the table names in a column
    """
    print("In database named %s, you have the following tables:" % database_name.rstrip('.db'))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_sequence ORDER BY name;")
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
        print("\tName\t\tType\n"
              "\t------\t\t------")
        for column in desired_table:
            print("\t" + column[1] + "\t\t" + str(column[2]).lower())
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

def detail_viewer(detail_type, input):
    show_list = find_matching_show(input)
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

    def help_tables(self):
        print('Lists the tables in the database.')

    def do_schema(self, inp):
        show_schema()

    def help_schema(self):
        print('Displays the schema for the database. Note: this is not the same as the SQL '
              'schema command that provides an exportable file to be used to recreate the database.')

    # TODO: REQUIRES FORMATTING
    def do_list(self, inp):
        if len(inp) != 0:
            list_table_content(inp)
        else:
            print('Invalid number of arguments. \nUsage:\n\tlist \'table_name\'')

    def help_list(self):
        print('Lists the content of a table. \nUsage:\n\tlist \'table_name\'')

    def do_runtime(self, inp):
        detail_viewer('runtime', inp)

    def help_runtime(self):
        print('Returns the runtime of a show and/or best matching shows. \nUsage:\n\truntime \'show_name\'')

    def do_status(self, inp):
        detail_viewer('status', inp)

    def help_status(self):
        print('Returns the on/off air status of a show and/or best matching shows. \nUsage:\n\tstatus \'show_name\'')

    def do_seasons(self, inp):
        detail_viewer('seasons', inp)

    def help_seasons(self):
        print('Returns the season count of a show and/or best matching shows. \nUsage:\n\tseasons \'show_name\'')

    def do_network(self, inp):
        detail_viewer('network', inp)

    def help_network(self):
        print('Returns the network a show and/or best matching shows is/are on. \nUsage:\n\tnetwork \'show_name\'')

    def do_genre(self, inp):
        detail_viewer('genre', inp)

    def help_genre(self):
        print('Returns the genre of a show and/or best matching shows. \nUsage:\n\tgenre \'show_name\'')

    def do_details(self, inp):
        detail_viewer('details', inp)

    def help_details(self):
        print('Returns the full details of a show and/or best matching shows, including: network, season count,'
              'runtime, genre, and on/off air status. \nUsage:\n\truntime \'show_name\'')

    def do_test_match(self, inp):
        find_matching_show(inp)

    # TODO: see if we actually need to follow the pycharm suggestion to make it static
    @staticmethod
    def do_columns(inp):
        params = inp.split()
        if len(params) == 2:
            full_column_return(params)
        elif len(params) == 1:
            list_columns(params[0])
        else:
            print("Invalid number of arguments.\nUsage:"
                  "\n\tcolumns 'table' - returns a list of columns in that table."
                  "\n\tcolumns 'table' 'column' - returns the contents of that column from that table.")
            return

    def help_columns(self):
        print("Returns either a list of the columns in a table or the contents.\nUsage:"
              "\n\tcolumns 'table' - returns a list of columns in that table."
              "\n\tcolumns 'table' 'column' - returns the contents of that column from that table.")

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
