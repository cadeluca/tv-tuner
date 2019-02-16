def query_writer(input_string):
    """
    takes a string and parse it into a sql query, also returns the columns queried
    :param input_string:
    :return: query_string, queried_columns
    """

    # splits the input into a list of strings
    inputs = str.split(input_string, " ")
    for i in range(len(inputs)):
        inputs[i] = inputs[i].lower()

    # list of all the columns in table
    columns = ["name", "runtime", "seasons", "status", "genre", "network", "ranking"]

    # list of columns in table if join
    join_columns = ["network", "ranking"]

    # selects when the join is neede
    if any([input in join_columns for input in inputs]):
        query_string = "SELECT * FROM shows LEFT JOIN networks ON shows.NetworkID = networks.NetworkID WHERE "
    else:
        # beginning for queries
        query_string = "SELECT * FROM shows WHERE "

    # keeps track of which columns are queried
    queried_columns = []

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
            queried_columns.append(inputs[counter])

            # checks for queries that can be compared, so columns of numbers
            if (inputs[counter] in ["runtime", "seasons", "ranking"]):

                # checks if > or < in query
                if (">" in inputs[counter + 1]) or ("<" in inputs[counter + 1]):
                    # sql query > or <
                    query_string += " " + inputs[counter + 1] + " "
                else:
                    # sql query
                    query_string += " = " + inputs[counter + 1] + " "
            else:

                # this code gets the whole query with the spaces
                name_query = inputs[counter + 1]
                # adds the rest of the query until a column name or the end of the list
                while (counter + 1 < len(inputs) - 1) and (inputs[counter + 2] not in columns):
                    name_query += " " + inputs[counter + 2]
                    counter += 1

                # sql query
                query_string += " LIKE '%" + name_query + "%' "

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

            # sql query
            query_string += "Name LIKE "
            query_string += "'%" + name_query + "%' "

            # increments counter by 1
            counter += 1
            # do not allow more queries with unspecified column
            unspecified_query = False
            # adds AND to allow more conditions to be tacked on
            if (counter < len(inputs)):
                query_string += " AND "

        # bad input
        else:
            print("Check your queries.")
            break

    return query_string, queried_columns