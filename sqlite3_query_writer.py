# Monolithic function to parse inputs and return a sqlite3 query
# Currently works with the sample.db
# Accepts as many parameters with specified column name as is input
# Accepts one parameter without specified column name
# For columns with numbers, allows comparison
# For columns with strings, allows wildcard comparisons
# Accepts parameters withe spaces
# I can add joins, will just be more monolith

def query_writer(input_string):
    # splits the input into a list of strings
    inputs = str.split(input_string, " ")

    # same beginning for all queries
    query_string = "SELECT * FROM tracks WHERE "

    # list of all the columns
    columns = ["Name", "Composer", "Milliseconds", "Bytes", "UnitPrice"]

    # counter for looping through the inputs
    counter = 0
    # switch for allowing one query with unspecified column, assumed to be name
    unspecified_query = True
    # loops through inputs
    while (counter < len(inputs)):

        # checks if the query in the columns
        if (inputs[counter] in columns):
            # put in column name
            query_string += inputs[counter]

            # checks for queries that can be compared, so columns of numbers
            if (inputs[counter] in ["Milliseconds", "Bytes"]):

                # checks if > or < in query
                if (">" in inputs[counter + 1]) or ("<" in inputs[counter + 1]):
                    # sql query > or <
                    query_string += " " + inputs[counter + 1] + " "
                else:
                    # sql query =
                    query_string += " = " + inputs[counter + 1] + " "
            else:

                # this code gets the whole query with the spaces
                name_query = inputs[counter + 1]
                # adds the rest of the query until a column name or the end of the list
                while (counter + 1 < len(inputs) - 1) and (inputs[counter + 2] not in columns):
                    name_query += " " + inputs[counter + 2]
                    counter += 1

                # checks for wildcard input
                if ("%" in inputs[counter + 1]) or ("_" in inputs[counter + 1]):
                    # sql query like
                    query_string += " LIKE '" + name_query + "' "
                else:
                    # sql query =
                    query_string += " = '" + name_query + "' "

            # increments counter by 2
            counter += 2
            # adds AND to allow more conditions to be tacked on
            if (counter < len(inputs)):
                query_string += " AND "

        # the one query with unspecified column, assumed to be name
        elif unspecified_query:

            # this code gets the whole query with the spaces
            name_query = inputs[counter]
            # adds the rest of the query until a column name or the end of the list
            while (counter < len(inputs) - 1) and (inputs[counter + 1] not in columns):
                name_query += " " + inputs[counter + 1]
                counter += 1

            # checks for wildcard inputs
            if ("%" in inputs[counter]) or ("_" in inputs[counter]):
                # sql query like
                query_string += "Name LIKE "
                query_string += "'" + name_query + "' "
            else:
                # sql query =
                query_string += "Name = "
                query_string += "'" + name_query + "' "

                # increments counter by 1
            counter += 1
            # do not allow more queries with unspecified column
            unspecified_query = False
            # adds AND to allow more conditions to be tacked on
            if (counter < len(inputs)):
                query_string += " AND "

        # bad input
        else:
            print("Too many queries without column names or column names do not exist")
            break

    return query_string