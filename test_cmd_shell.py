#!/usr/bin/env python

"""
CS 205: Warm-up Project
UVM Spring Semester 2019

Team members:
Christian DeLuca
Jiangyong Yu
Megan Doyle
Dale Larie

CLI for data on television shows
"""

import sqlite3
from cmd import Cmd
from sqlite3 import Error
import cli_animations
from sqlite3_query_writer import query_writer

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
    results = cur.execute("SELECT name FROM shows WHERE name LIKE '%"+searched_string+"%';").fetchall()
    results_list = []
    for result in results:
        if debug:
            print(result[0])
        results_list.append(result[0])
    conn.commit()
    # if debug:
    #     print(results_list)
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
    cur.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
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
    if len(desired_table) != 0:
        print("The table '%s' has the following columns:" % desired_table_name)
        print("\tName\t\tType\n"
              "\t------\t\t\t------")
        for column in desired_table:
            print("\t" + column[1] + "\t\t\t" + str(column[2]).lower())
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
def detail_viewer(detail_type, inp):
    show_list = find_matching_show(inp)
    if len(show_list) <= 0:
        print("No shows in database containing '%s'" % inp)
    else:
        cur = conn.cursor()
        if len(show_list) == 1:
            print("Your query '%s' returned one result:" % inp)
            show = show_list[0]
            if detail_type != 'details' and detail_type != 'network':
                result = cur.execute("SELECT %s FROM shows WHERE name = '%s'" % (detail_type, show)).fetchone()
                if detail_type == 'runtime':
                    print(("\t- %s has a runtime of " + str(result[0]) + " minutes") % show)
                elif detail_type == 'seasons':
                    print(("\t- %s has " + str(result[0]) + " seasons") % show)
                elif detail_type == 'status':
                    print(("\t- %s is " + str(result[0]).lower() + " the air") % show)
                else:
                    print(("\t- %s is a " + result[0]) % show)
            elif detail_type == 'details':
                result = cur.execute("SELECT * FROM shows LEFT JOIN networks ON shows.NetworkID=networks.NetworkID "
                                     "WHERE name = '%s'" % show).fetchone()
                print("Details for " + result[0] + ":")
                print("\t- Runtime: " + str(result[1]) + " minutes")
                print("\t- Seasons: " + str(result[2]))
                print("\t- Status: " + result[3] + " the air")
                print("\t- Genre: " + result[4])
                print("\t- Network: " + result[7])

            else:
                result = cur.execute("SELECT %s FROM shows LEFT JOIN networks ON shows.NetworkID=networks.NetworkID "
                                     "WHERE name = '%s'" % (detail_type, show)).fetchone()
                print(("\t- %s is on " + result[0]) % show)

        else:
            print("Your query '%s' returned multiple results:" % inp)
            if detail_type != 'details' and detail_type != 'network':
                for show in show_list:
                    result = cur.execute("SELECT %s FROM shows WHERE name='%s';" % (detail_type, show)).fetchone()
                    if detail_type == 'runtime':
                        print(("\t- %s has a runtime of " + str(result[0]) + " minutes") % show)
                    elif detail_type == 'seasons':
                        print(("\t- %s has " + str(result[0]) + " seasons") % show)
                    elif detail_type == 'status':
                        print(("\t- %s is " + str(result[0]).lower() + " the air") % show)
                    else:
                        print(("\t- %s is a " + result[0]) % show)
            elif detail_type == 'details':
                for show in show_list:
                    result = cur.execute("SELECT * FROM shows LEFT JOIN networks ON shows.NetworkID=networks.NetworkID "
                                         "WHERE name = '%s'" % show).fetchone()
                    print("Details for " + result[0] + ":")
                    print("\t- Runtime: " + str(result[1]) + " minutes")
                    print("\t- Seasons: " + str(result[2]))
                    print("\t- Status: " + result[3] + " the air")
                    print("\t- Genre: " + result[4])
                    print("\t- Network: " + result[7] + "\n")
            else:
                for show in show_list:
                    result = cur.execute("SELECT %s FROM shows LEFT JOIN networks ON shows.NetworkID=networks.NetworkID "
                                         "WHERE name = '%s'" % (detail_type, show)).fetchone()
                    print(("\t- %s is on " + result[0]) % show)
        conn.commit()


# this uses that big function.
def search(input_string):
    """
    Search function, takes some paramters and returns a formatted table that shows those columns
    :param input_string:
    :return:
    """

    cursor = conn.cursor()

    # getting the query and columns
    query, queried_columns = query_writer(input_string)

    # formatting for the print table
    column_names = ["Name", "Runtime", "Seasons", "Status", "Genre", "NID", "NID", "Network", "Ranking"]
    # spacing for the columns
    column_widths = ["30", "9", "9", "8", "8", "8", "8", "10", "8"]

    try:
        # querying the database
        cursor.execute(query)
        results = cursor.fetchall()

        # keeps track of which indices are queired, for the table printing
        queried_indices = [0]

        # fills the queried indices
        for i in range(len(column_names)):
            if column_names[i].lower() in queried_columns:
                queried_indices.append(i)

        # prints the column names
        for i in range(len(column_names)):
            if i in queried_indices:
                print(format(column_names[i], column_widths[i] + "s"), end="")

        print("\n")

        # prints the rows
        for i in range(len(results)):
            for j in range(len(results[0])):
                if j in queried_indices:
                    print(format(str(results[i][j]), column_widths[j] + "s"), end="")
            print("\n")

    # if the query failed
    except:
        print("No results, check your query string")


#
# End Simple grammar functions
#


#
# Complex grammar functions
#

# TODO: Place the search function here

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

    def do_search(self, inp):
        search(inp)

    def do_runtime(self, inp):
        if len(inp) > 0:
            detail_viewer('runtime', inp)
        else:
            print("Invalid number of arguments.\nUsage:"
                  "\n\truntime 'show' - returns the runtime of any matching shows from your inputted string.")

    def help_runtime(self):
        print('Returns the runtime of a show and/or best matching shows. \nUsage:\n\truntime \'show_name\'')

    def do_status(self, inp):
        if len(inp) > 0:
            detail_viewer('status', inp)
        else:
            print("Invalid number of arguments.\nUsage:"
                  "\n\tstatus 'show' - returns the air status of any matching shows from your inputted string.")

    def help_status(self):
        print('Returns the on/off air status of a show and/or best matching shows. \nUsage:\n\tstatus \'show_name\'')

    def do_seasons(self, inp):
        if len(inp) > 0:
            detail_viewer('seasons', inp)
        else:
            print("Invalid number of arguments.\nUsage:"
                  "\n\tseasons 'show' - returns the number of seasons of any matching shows from your inputted string.")

    def help_seasons(self):
        print('Returns the season count of a show and/or best matching shows. \nUsage:\n\tseasons \'show_name\'')

    def do_network(self, inp):
        if len(inp) > 0:
            detail_viewer('network', inp)
        else:
            print("Invalid number of arguments.\nUsage:"
                  "\n\tnetwork 'show' - returns the network of any matching shows from your inputted string.")

    def help_network(self):
        print('Returns the network a show and/or best matching shows is/are on. \nUsage:\n\tnetwork \'show_name\'')

    def do_genre(self, inp):
        if len(inp) > 0:
            detail_viewer('genre', inp)
        else:
            print("Invalid number of arguments.\nUsage:"
                  "\n\tgenre 'show' - returns the genre of any matching shows from your inputted string.")

    def help_genre(self):
        print('Returns the genre of a show and/or best matching shows. \nUsage:\n\tgenre \'show_name\'')

    def do_details(self, inp):
        if len(inp) > 0:
            detail_viewer('details', inp)
        else:
            print("Invalid number of arguments.\nUsage:"
                  "\n\tdetails 'show' - returns the details of any matching shows, including: network, season count,"
                  " runtime, genre, and on/off air status from your inputted string.")

    def help_details(self):
        print('Returns the full details of a show and/or best matching shows, including: network, season count,'
              'runtime, genre, and on/off air status. \nUsage:\n\truntime \'show_name\'')

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
    database_name = "tv_tuner.db"
    # create a database connection
    conn = create_connection(database_name)
    with conn:
        if debug:
            print("connected!")
        MainPrompt().cmdloop(cli_animations.intro())
