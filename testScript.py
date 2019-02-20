import sys
import test_cmd_shell
import io
import subprocess

# try:
#     import StringIO
# except ImportError:
#     from io import StringIO

# Debug variable
debug = True

        # def test_foo(inp):
        #
        #     capturedOutput = StringIO.StringIO()  # Create StringIO object
        #     sys.stdout = capturedOutput  # and redirect stdout.
        #     test_cmd_shell.MainPrompt().onecmd(inp) # Call unchanged function.
        #     sys.stdout = sys.__stdout__  # Reset redirect.
        #     # print 'Captured', capturedOutput.getvalue()  # Now works as before.

            # return capturedOutput.getvalue()
def test_foo(inp):
    captured_output = io.StringIO()  # Create StringIO object

    sys.stdout = captured_output  # and redirect stdout.
    test_cmd_shell.MainPrompt().onecmd(inp)
    sys.stdout = sys.__stdout__  # Reset redirect.
    # print 'Captured', captured_output.getvalue()  # Now works as before.

    return captured_output.getvalue()


def test_exit():
    passed = True
    if test_foo('q') != 'Tune in next time!':
        print("Failed exit 1")
        passed = False

    if test_foo('x') != 'Tune in next time!':
        print("Failed exit 2")
        passed = False

    if test_foo("exit") != 'Tune in next time!':
        print("Failed exit 3")
        passed = False

    return passed

def test_help():
    passed = True
    # testing help
    if test_foo('help') !="\nDocumented commands (type help <topic>):\n========================================\ncolumns  exit   help  network  schema  seasons  tables\ndetails  genre  list  runtime  search  status \n\n":
        print("Failed help 1")
        passed = False
    # testong ? to pull up help
    if test_foo('?') !="\nDocumented commands (type help <topic>):\n========================================\ncolumns  exit   help  network  schema  seasons  tables\ndetails  genre  list  runtime  search  status \n\n":
        print("Failed help 2")
        passed = False
    # testing help exit
    if test_foo('help exit') != 'Exits the application. Shorthand: \'x\' \'q\' \'Ctrl-D\'.\n':
        print("Failed help exit")
        passed = False
    # testing schema help
    if test_foo("help schema") != "Displays the schema for the database. Note: this is not the same as the SQL schema command that provides an exportable file to be used to recreate the database.\n":
        passed = False
        print("failed help schema")

    return passed


def test_genre():
    passed = True
    # testing genre of known lower case input
    if test_foo("genre house") !="Your query 'house' returned one result:\n\t- House Hunters is a Reality show\n":
        passed = False
        print("Failed genre 0")
    #     testing genre of capticalized input
    if test_foo("genre HoUse") !="Your query 'HoUse' returned one result:\n\t- House Hunters is a Reality show\n":
        passed = False
        print("Failed genre 1")
    #     testing genre incorrect use
    if test_foo('genre') !=("Invalid number of arguments.\nUsage:"
                  "\n\tgenre 'show' - returns the genre of any matching shows from your inputted string.\n"):
        passed = False
        print("Failed genre 2")
    #     testing misspelled or incomplete words
    if test_foo('genre hosu') != "No shows in database containing 'hosu'\n":
        passed = False
        print("failed genre 3")
    #
    return passed


def test_network():
    # testing correct use
    passed = True
    if test_foo("network HoUse") !="Your query 'HoUse' returned one result:\n\t- House Hunters is on HGTV\n":
        passed = False
        print("Failed network 0")
    if test_foo("network house") !="Your query 'house' returned one result:\n\t- House Hunters is on HGTV\n":
        passed = False
        print("Failed network 1")
    #     testing incorrect use
    if test_foo('network') !=("Invalid number of arguments.\nUsage:"
                  "\n\tnetwork 'show' - returns the network of any matching shows from your inputted string.\n"):
        passed = False
        print("Failed network 2")
    #     testing misspelled or incomplete
    if test_foo('genre hosu') != "No shows in database containing 'hosu'\n":
        passed = False
        print("failed network 3")
    #
    return passed


def test_schema():
    passed = True
    # testing that schema comes up correctly
    if test_foo('schema') != ("Displaying database schema:\n\nTable Name: networks\n(0, 'NetworkID', 'INTEGER', 0, None, 0)"
                              "\n(1, 'Network', 'VARCHAR (20)', 0, None, 1)\n(2, 'Ranking', 'INTEGER', 0, None, 0)\n\n\n"
                              "Table Name: shows\n(0, 'Name', 'VARCHAR (40)', 0, None, 1)\n(1, 'Runtime', 'INTEGER', 0, None, 0)"
                              "\n(2, 'Seasons', 'INTEGER', 0, None, 0)\n(3, 'Status', 'VARCHAR (20)', 0, None, 0)\n"
                              "(4, 'Genre', 'VARCHAR (20)', 0, None, 0)\n(5, 'NetworkID', 'INTEGER', 0, None, 0)\n\n\n"):
        passed = False
        print("failed schema 1")

    return passed


def test_seasons():
    passed = True
    # testing incorrect use of seasons
    if test_foo("seasons") != ("Invalid number of arguments.\nUsage:"""
                               "\n\tseasons 'show' - returns the number of seasons of any matching shows from your inputted string.\n"):
        passed = False
        print("failed seasons 1")
    #     testing correct use with caps
    if test_foo("seasons House") != ("Your query 'House' returned one result:"""
                                     "\n\t- House Hunters has 162 seasons\n"):
        passed = False
        print("Failed seasons 2")
        # testing correct use without caps
    if test_foo("seasons house") != ("Your query 'house' returned one result:"""
                                     "\n\t- House Hunters has 162 seasons\n"):
        passed = False
        print("Failed seasons 3")
    #     testing correct use bad spelling or incomplete
    if test_foo('seasons hosu') != "No shows in database containing 'hosu'\n":
        passed = False
        print("failed seasons 4")

    return passed


def test_tables():
    passed = True
    # testing correct use of tables
    if test_foo("tables") != ("In database named tv_tuner, you have the following tables:\n\tnetworks\n\tshows\n"):
        passed = False
        print("failed tables 1")

    return passed

def test_details():
    passed = True
    # testing incorrect use of details
    if test_foo("details") != ("Invalid number of arguments.\nUsage:"
            "\n\tdetails 'show' - returns the details of any matching shows, including: network, season count, runtime, "
            "genre, and on/off air status from your inputted string.\n"):
        passed = False
        print("failed details 1")
    #     testing correct use lower case
    if test_foo("details house") != ("Your query 'house' returned one result:"
                                     "\nDetails for House Hunters:"
                                     "\n\t- Runtime: 30 minutes"
                                     "\n\t- Seasons: 162"
                                     "\n\t- Status: On the air"
                                     "\n\t- Genre: Reality"
                                     "\n\t- Network: HGTV\n"):
        passed = False
        print("failed details 2")

    # testing correct use caps
    if test_foo("details HoUse") != ("Your query 'HoUse' returned one result:"
                                    "\nDetails for House Hunters:"
                                    "\n\t- Runtime: 30 minutes"
                                    "\n\t- Seasons: 162"
                                    "\n\t- Status: On the air"
                                    "\n\t- Genre: Reality"
                                    "\n\t- Network: HGTV\n"):
        passed = False
        print("failed details 3")
    # testing correct use bad spelling
    if test_foo("details hosu") != "No shows in database containing 'hosu'\n":
        passed = False
        print("failed details 4")

    return passed

def test_columns():
    passed = True
    # testing incorrect use
    if test_foo("columns") != ("Invalid number of arguments.\nUsage:"
                               "\n\tcolumns 'table' - returns a list of columns in that table."
                               "\n\tcolumns 'table' 'column' - returns the contents of that column from that table.\n"):
        passed = False
        print("Failed Columns 1")
    #     testing correct use shows
    if test_foo("columns shows") != ("The table 'shows' has the following columns:"
                                     "\n\tName\t\tType"
                                     "\n\t------\t\t\t------"
                                     "\n\tName\t\t\tvarchar (40)"
                                     "\n\tRuntime\t\t\tinteger"
                                     "\n\tSeasons\t\t\tinteger"
                                     "\n\tStatus\t\t\tvarchar (20)"
                                     "\n\tGenre\t\t\tvarchar (20)"
                                     "\n\tNetworkID\t\t\tinteger\n"):
        passed = False
        print("Failed Columns 2")
    # testin correct use networks
    if test_foo("columns networks") != ("The table 'networks' has the following columns:"
                                        "\n\tName\t\tType"
                                        "\n\t------\t\t\t------"
                                        "\n\tNetworkID\t\t\tinteger"
                                        "\n\tNetwork\t\t\tvarchar (20)"
                                        "\n\tRanking\t\t\tinteger\n"):
        passed = False
        print("Failed Columns 3")
    #     testing columns caps
    if test_foo("columns Networks") != ("The table 'Networks' has the following columns:"
                                        "\n\tName\t\tType"
                                        "\n\t------\t\t\t------"
                                        "\n\tNetworkID\t\t\tinteger"
                                        "\n\tNetwork\t\t\tvarchar (20)"
                                        "\n\tRanking\t\t\tinteger\n"):
        passed = False
        print("Failed Columns 3a")
    # testing correct use incomplete/bad spelling
    if test_foo("columns net") != "The table 'net' is not in the database.\n":
        passed = False
        print("failed Columns 4")

    if test_foo("columns networks networkid") != "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18" \
                                                 "\n19\n20\n21\n22\n23\n24\n25\n26\n27\n28\n29\n30\n":
        passed = False
        print("Failed Columns 5")

    if test_foo("columns networks network") != ("A&E\nABC\nAMC\nBoomerang\nBravo\nCBS\nComedy Central\nDiscovery Channel"
                                                "\nE!\nFX\nFXX\nFood Network\nFox\nHGTV\nHistory Channel\nHulu\nLifetime"
                                                "\nMTV\nNBC\nNational Geographic\nNetflix\nNickolodean\nOxygen\nPBS"
                                                "\nShowtime\nTLC\nTNT\nUSA\nVH1\ntruTV\n"):
        passed = False
        print("Failed Columns 6")

    if test_foo("columns networks ranking") != "23\n9\n3\n6\n4\n30\n55\n40\n21\n1\n35\n2\n20\n19\n10\n13\34\n67\n11\n54" \
                                               "\n66\n42\n70\n71\n89\n45\n77\n53\n24\n102\n":
        passed = False
        print("Failed Column 7")

    if test_foo("columns shows name") != ("911\nAlways Sunny in Philidelphia\nAmerican Horror Story" 
                                         "\nAvatar the Last Airbender\nBlack Mirror\nBob's Burgers\nBreaking Bad" 
                                         "\nBroad City\nBrooklyn Nine Nine\nCatfish\nChopped\nDear White People" 
                                         "\nFixer Upper\nForensic Files\nFresh Off the Boat\nFuturama\nHell's Kitchen" 
                                         "\nHouse Hunters\nJeapardy\nKilling Eve\nKitchen Nightmares\nNailed It!" 
                                         "\nNew Girl\nParks and Recreation\nQueer Eye\nScream Queens\nShameless" 
                                         "\nThe Bachelor\nThe Mindy Project\nYou\n"):
        passed = False
        print("Failed coloumns 8")

    if test_foo("columns shows runtime") != ("30\n30\n60\n30\n60\n30\n30\n60\n60\n90\n60\n60\n60\n60\n60\n30\n60\n30"
                                             "\n30\n30\n30\n30\n45\n60\n60\n60\n30\n30\n50\n30\n"):
        passed = False
        print("failed columns 9")

    if test_foo("columns shows seasons") != ("12\n162\n5\n5\n1\n7\n6\n6\n18\n23\n10\n40\n7\n2\n2\n6\n8\n7\n8\n5\n11\n35"
                                             "\n2\n5\n4\n1\n9\n2\n2\n3\n"):
        passed = False
        print("failed columns 10")

    if test_foo("columns shows status") !=("On\nOn\nOff\nOn\nOn\nOff\nOn\nOff\nOn\nOn\nOn\nOn\nOff\nOn\nOff\nOff\nOn"
                                           "\nOff\nOff\nOn\nOff\nOn\nOn\nOff\nOn\nOn\nOn\nOn\nOn\nOff\n"):
        passed = False
        print("failed columns 11")

    if test_foo("columns shows genre") != ("Comedy\nReality\nReality\nComedy\nThriller\nComedy\nComedy\nReality"
                                           "\nCompetition\nReality\nDrama\nCompetition\nReality\nDrama\nThriller"
                                           "\nComedy\nHorror\nComedy\nComedy\nComedy\nCrime\nGame show\nCompetition"
                                           "\nDrama\nHorror\nThriller\nComedy\nDrama\nReality\nComedy\n"):
        passed = False
        print("Failed columns 12")

    if test_foo("columns shows networkid") != ("1\n2\n2\n3\n4\n5\n5\n5\n5\n3\n6\n7\n8\n5\n5\n4\n9\n5\n10\n11\n10\n10"
                                               "\n12\n13\n12\n12\n5\n12\n12\n14\n"):
        passed = False
        print("failed columns 13")

    if test_foo("columns shows net") != "no such column: net\n":
        passed = False
        print("failed columns 14")

    if test_foo("columns networks net") != "no such column: net\n":
        passed = False
        print("failed columns 15")

    return passed


def test_list():
    passed = True
    if test_foo("list") != ('Invalid number of arguments. \nUsage:'
                            '\n\tlist \'table_name\'\n'):
        passed = False
        print("failed list 1")

    if test_foo("list shows") != ("['Name', 'Runtime', 'Seasons', 'Status', 'Genre', 'NetworkID']"
                                  "\n('Always Sunny in Philidelphia', 30, 12, 'On', 'Comedy', 1)"
                                  "\n('House Hunters', 30, 162, 'On', 'Reality', 2)"
                                  "\n('Fixer Upper', 60, 5, 'Off', 'Reality', 2)"
                                  "\n('Fresh Off the Boat', 30, 5, 'On', 'Comedy', 3)"
                                  "\n('Killing Eve', 60, 1, 'On', 'Thriller', 4)"
                                  "\n('Futurama', 30, 7, 'Off', 'Comedy', 5)"
                                  "\n('Brooklyn Nine Nine', 30, 6, 'On', 'Comedy', 5)"
                                  "\n('Kitchen Nightmares', 60, 6, 'Off', 'Reality', 5)"
                                  "\n(\"Hell's Kitchen\", 60, 18, 'On', 'Competition', 5)"
                                  "\n('The Bachelor', 90, 23, 'On', 'Reality', 3)"
                                  "\n('Shameless', 60, 10, 'On', 'Drama', 6)"
                                  "\n('Chopped', 60, 40, 'On', 'Competition', 7)"
                                  "\n('Catfish', 60, 7, 'Off', 'Reality', 8)"
                                  "\n('911', 60, 2, 'On', 'Drama', 5)"
                                  "\n('Scream Queens', 60, 2, 'Off', 'Thriller', 5)"
                                  "\n('The Mindy Project', 30, 6, 'Off', 'Comedy', 4)"
                                  "\n('American Horror Story', 60, 8, 'On', 'Horror', 9)"
                                  "\n('New Girl', 30, 7, 'Off', 'Comedy', 5)"
                                  "\n('Parks and Recreation', 30, 8, 'Off', 'Comedy', 10)"
                                  "\n('Broad City', 30, 5, 'On', 'Comedy', 11)"
                                  "\n('Forensic Files', 30, 11, 'Off', 'Crime', 10)"
                                  "\n('Jeapardy', 30, 35, 'On', 'Game show', 10)"
                                  "\n('Nailed It!', 45, 2, 'On', 'Competition', 12)"
                                  "\n('Breaking Bad', 60, 5, 'Off', 'Drama', 13)"
                                  "\n('Black Mirror', 60, 4, 'On', 'Horror', 12)"
                                  "\n('You', 60, 1, 'On', 'Thriller', 12)"
                                  "\n(\"Bob's Burgers\", 30, 9, 'On', 'Comedy', 5)"
                                  "\n('Dear White People', 30, 2, 'On', 'Drama', 12)"
                                  "\n('Queer Eye', 50, 2, 'On', 'Reality', 12)"
                                  "\n('Avatar the Last Airbender', 30, 3, 'Off', 'Comedy', 14)\n"):
        passed = False
        print("failed list 2")

    if test_foo("list networks") != ("['NetworkID', 'Network', 'Ranking']\n(1, 'FXX', 23)\n(2, 'HGTV', 9)"
                                     "\n(3, 'ABC', 3)\n(4, 'Hulu', 6)\n(5, 'Fox', 4)\n(6, 'Showtime', 30)"
                                     "\n(7, 'Food Network', 55)\n(8, 'MTV', 40)\n(9, 'FX', 21)\n(10, 'NBC', 1)"
                                     "\n(11, 'Comedy Central', 35)\n(12, 'Netflix', 2)\n(13, 'AMC', 20)"
                                     "\n(14, 'Nickolodean', 19)\n"):
        passed = False
        print("Failed list 3")

    if test_foo("list net") != "No matching table 'net'\n":
        passed = False
        print("Failed list 4")

    return passed


def test_runtime():
    passed = True
    if test_foo("runtime") != ("Invalid number of arguments.\nUsage:\n\truntime "
                               "'show' - returns the runtime of any matching shows from your inputted string.\n"):
        passed = False
        print("failed runtime 1")

    if test_foo("runtime house") != ("Your query 'house' returned one result:\n\t- House Hunters has a runtime of "
                                     "30 minutes\n"):
        passed = False
        print("failed runtime 2")

    return passed


def test_search():
    passed = True
    if test_foo("search always") != "Name                          \n\nAlways Sunny in Philidelphia  \n\n":
        passed = False
        print("failed Search 1")

    if test_foo("search") != ("Name                          \n\nAlways Sunny in Philidelphia  "
                              "\n\nHouse Hunters                 \n\nFixer Upper                   "
                              "\n\nFresh Off the Boat            \n\nKilling Eve                   "
                              "\n\nFuturama                      \n\nBrooklyn Nine Nine            "
                              "\n\nKitchen Nightmares            \n\nHell's Kitchen                "
                              "\n\nThe Bachelor                  \n\nShameless                     "                    
                              "\n\nChopped                       \n\nCatfish                       "                       
                              "\n\n911                           \n\nScream Queens                 "                 
                              "\n\nThe Mindy Project             \n\nAmerican Horror Story         "         
                              "\n\nNew Girl                      \n\nParks and Recreation          "          
                              "\n\nBroad City                    \n\nForensic Files                "                
                              "\n\nJeapardy                      \n\nNailed It!                    "                    
                              "\n\nBreaking Bad                  \n\nBlack Mirror                  "
                              "\n\nYou                           \n\nBob's Burgers                 "
                              "\n\nDear White People             \n\nQueer Eye                     "
                              "\n\nAvatar the Last Airbender     \n\n"):
        passed = False
        print("failed Search 2")

    if test_foo("search runtime") != ("Name                          Runtime  \n\nAlways Sunny in Philidelphia  30       "
                                      "\n\nHouse Hunters                 30       \n\nFixer Upper                   60       "
                                      "\n\nFresh Off the Boat            30       \n\nKilling Eve                   60       "
                                      "\n\nFuturama                      30       \n\nBrooklyn Nine Nine            30       "
                                      "\n\nKitchen Nightmares            60       \n\nHell's Kitchen                60       "
                                      "\n\nThe Bachelor                  90       \n\nShameless                     60       "
                                      "\n\nChopped                       60       \n\nCatfish                       60       "
                                      "\n\n911                           60       \n\nScream Queens                 60       "
                                      "\n\nThe Mindy Project             30       \n\nAmerican Horror Story         60       "
                                      "\n\nNew Girl                      30       \n\nParks and Recreation          30       "
                                      "\n\nBroad City                    30       \n\nForensic Files                30       "
                                      "\n\nJeapardy                      30       \n\nNailed It!                    45       "
                                      "\n\nBreaking Bad                  60       \n\nBlack Mirror                  60       "
                                      "\n\nYou                           60       \n\nBob's Burgers                 30       "
                                      "\n\nDear White People             30       \n\nQueer Eye                     50       "
                                      "\n\nAvatar the Last Airbender     30       \n\n"):
        passed = False
        print("failed search 3")

    if test_foo("search runtime <31") != ("Name                          Runtime  \n\nAlways Sunny in Philidelphia  30       "
                                          "\n\nHouse Hunters                 30       \n\nFresh Off the Boat            30       "
                                          "\n\nFuturama                      30       \n\nBrooklyn Nine Nine            30       "
                                          "\n\nThe Mindy Project             30       \n\nNew Girl                      30       "
                                          "\n\nParks and Recreation          30       \n\nBroad City                    30       "
                                          "\n\nForensic Files                30       \n\nJeapardy                      30       "
                                          "\n\nBob's Burgers                 30       \n\nDear White People             30       "
                                          "\n\nAvatar the Last Airbender     30       \n\n"):
        passed = False
        print("failed search 4")

    if test_foo("search runtime 50") != "Name                          Runtime  \n\nQueer Eye                     50       \n\n":
        passed = False
        print("failed search 5")

    if test_foo("search runtime >60") !="Name                          Runtime  \n\nThe Bachelor                  90       \n\n":
        passed = False
        print("failed search 6")

    # if test_foo("search seasons") !=("Name                          Seasons  \n\nAlways Sunny in Philidelphia  12       "
    #                                   "\n\nHouse Hunters                 162      \n\nFixer Upper                   5        "                                      "\n\nHouse Hunters                 162      \n\nFixer Upper                   5        "
    #                                   "\n\nFresh Off the Boat            5        \n\nKilling Eve                   1        "
    #                                   "\n\nFuturama                      7        \n\nBrooklyn Nine Nine            6        "
    #                                   "\n\nKitchen Nightmares            6        \n\nHell's Kitchen                18       "
    #                                   "\n\nThe Bachelor                  23       \n\nShameless                     10       "
    #                                   "\n\nChopped                       40       \n\nCatfish                       7        "
    #                                   "\n\n911                           2        \n\nScream Queens                 2        "
    #                                   "\n\nThe Mindy Project             6        \n\nAmerican Horror Story         8        "
    #                                   "\n\nNew Girl                      7        \n\nParks and Recreation          8        "
    #                                   "\n\nBroad City                    5        \n\nForensic Files                11       "
    #                                   "\n\nJeapardy                      35       \n\nNailed It!                    2        "
    #                                   "\n\nBreaking Bad                  5        \n\nBlack Mirror                  4        "
    #                                   "\n\nYou                           1        \n\nBob's Burgers                 9        "
    #                                   "\n\nDear White People             2        \n\nQueer Eye                     2        "
    #                                   "\n\nAvatar the Last Airbender     3        \n\n"):
    #
    #     passed = False
    #     print("failed search 7")

    if test_foo("search seasons <2") != ("Name                          Seasons  \n\nKilling Eve                   1        "
                                         "\n\nYou                           1        \n\n"):
        passed = False
        print("failed search 8")

    if test_foo("search seasons >100") != "Name                          Seasons  \n\nHouse Hunters                 162      \n\n":
        passed = False
        print("Failed search 9")

    if test_foo("search seasons 162") != "Name                          Seasons  \n\nHouse Hunters                 162      \n\n":
        passed = False
        print("failed search 10")

    if test_foo("search seasons a") != "No results, check your query string\n":
        passed = False
        print("Failed search 11")

    if test_foo("search status") != ("Name                          Status  \n\nAlways Sunny in Philidelphia  On      "
                                     "\n\nHouse Hunters                 On      \n\nFixer Upper                   Off     "
                                     "\n\nFresh Off the Boat            On      \n\nKilling Eve                   On      "
                                     "\n\nFuturama                      Off     \n\nBrooklyn Nine Nine            On      "
                                     "\n\nKitchen Nightmares            Off     \n\nHell's Kitchen                On      "
                                     "\n\nThe Bachelor                  On      \n\nShameless                     On      "
                                     "\n\nChopped                       On      \n\nCatfish                       Off     "
                                     "\n\n911                           On      \n\nScream Queens                 Off     "
                                     "\n\nThe Mindy Project             Off     \n\nAmerican Horror Story         On      "
                                     "\n\nNew Girl                      Off     \n\nParks and Recreation          Off     "
                                     "\n\nBroad City                    On      \n\nForensic Files                Off     "
                                     "\n\nJeapardy                      On      \n\nNailed It!                    On      "
                                     "\n\nBreaking Bad                  Off     \n\nBlack Mirror                  On      "
                                     "\n\nYou                           On      \n\nBob's Burgers                 On      "
                                     "\n\nDear White People             On      \n\nQueer Eye                     On      "
                                     "\n\nAvatar the Last Airbender     Off     \n\n"):
        passed = False
        print("failed search 12")

    if test_foo("search status on") != ("Name                          Status  \n\nAlways Sunny in Philidelphia  On      "
                                        "\n\nHouse Hunters                 On      \n\nFresh Off the Boat            On      "
                                        "\n\nKilling Eve                   On      \n\nBrooklyn Nine Nine            On      "
                                        "\n\nHell's Kitchen                On      \n\nThe Bachelor                  On      "
                                        "\n\nShameless                     On      \n\nChopped                       On      "
                                        "\n\n911                           On      \n\nAmerican Horror Story         On      "
                                        "\n\nBroad City                    On      \n\nJeapardy                      On      "
                                        "\n\nNailed It!                    On      \n\nBlack Mirror                  On      "
                                        "\n\nYou                           On      \n\nBob's Burgers                 On      "
                                        "\n\nDear White People             On      \n\nQueer Eye                     On      \n\n"):
        passed = False
        print("failed search 13")

    if test_foo("search status off") != ("Name                          Status  \n\nFixer Upper                   Off     "
                                         "\n\nFuturama                      Off     \n\nKitchen Nightmares            Off     "
                                         "\n\nCatfish                       Off     \n\nScream Queens                 Off     "
                                         "\n\nThe Mindy Project             Off     \n\nNew Girl                      Off     "
                                         "\n\nParks and Recreation          Off     \n\nForensic Files                Off     "
                                         "\n\nBreaking Bad                  Off     \n\nAvatar the Last Airbender     Off     \n\n"):
        passed = False
        print("failed search 14")

    if test_foo("search status a") !=  "No results, check your query string\n":
        passed = False
        print("failed search 15")

    if test_foo("search genre") != ("Name                          Genre   \n\nAlways Sunny in Philidelphia  Comedy  "
                                    "\n\nHouse Hunters                 Reality \n\nFixer Upper                   Reality "
                                    "\n\nFresh Off the Boat            Comedy  \n\nKilling Eve                   Thriller"
                                    "\n\nFuturama                      Comedy  \n\nBrooklyn Nine Nine            Comedy  "
                                    "\n\nKitchen Nightmares            Reality \n\nHell's Kitchen                Competition"
                                    "\n\nThe Bachelor                  Reality \n\nShameless                     Drama   "
                                    "\n\nChopped                       Competition\n\nCatfish                       Reality "
                                    "\n\n911                           Drama   \n\nScream Queens                 Thriller"
                                    "\n\nThe Mindy Project             Comedy  \n\nAmerican Horror Story         Horror  "
                                    "\n\nNew Girl                      Comedy  \n\nParks and Recreation          Comedy  "
                                    "\n\nBroad City                    Comedy  \n\nForensic Files                Crime   "
                                    "\n\nJeapardy                      Game show\n\nNailed It!                    Competition"
                                    "\n\nBreaking Bad                  Drama   \n\nBlack Mirror                  Horror  "
                                    "\n\nYou                           Thriller\n\nBob's Burgers                 Comedy  "
                                    "\n\nDear White People             Drama   \n\nQueer Eye                     Reality "
                                    "\n\nAvatar the Last Airbender     Comedy  \n\n"):
        passed = False
        print("failed search 16")

    if test_foo("search genre game show") != "Name                          Genre   \n\nJeapardy                      Game show\n\n":
        passed = False
        print("Failed search 17")

    if test_foo("search genre q") != "No results, check your query string\n":
        passed = False
        print("failed search 18")

    if test_foo("search network") != ("Name                          Network   \n\nAlways Sunny in Philidelphia  FXX       "
                                      "\n\nHouse Hunters                 HGTV      \n\nFixer Upper                   HGTV      "
                                      "\n\nFresh Off the Boat            ABC       \n\nKilling Eve                   Hulu      "
                                      "\n\nFuturama                      Fox       \n\nBrooklyn Nine Nine            Fox       "
                                      "\n\nKitchen Nightmares            Fox       \n\nHell's Kitchen                Fox       "
                                      "\n\nThe Bachelor                  ABC       \n\nShameless                     Showtime  "
                                      "\n\nChopped                       Food Network\n\nCatfish                       MTV       "
                                      "\n\n911                           Fox       \n\nScream Queens                 Fox       "
                                      "\n\nThe Mindy Project             Hulu      \n\nAmerican Horror Story         FX        "
                                      "\n\nNew Girl                      Fox       \n\nParks and Recreation          NBC       "
                                      "\n\nBroad City                    Comedy Central\n\nForensic Files                NBC       "
                                      "\n\nJeapardy                      NBC       \n\nNailed It!                    Netflix   "
                                      "\n\nBreaking Bad                  AMC       \n\nBlack Mirror                  Netflix   "
                                      "\n\nYou                           Netflix   \n\nBob's Burgers                 Fox       "
                                      "\n\nDear White People             Netflix   \n\nQueer Eye                     Netflix   "
                                      "\n\nAvatar the Last Airbender     Nickolodean\n\n"):
        passed = False
        print("failed search 19")

    if test_foo("search network food network") != "Name                          Network   \n\nChopped                       Food Network\n\n":
        passed = False
        print("failed search 20")

    if test_foo("search network q") != "No results, check your query string\n":
        passed = False
        print("failed search 21")

    if test_foo("search ranking") != ("Name                          Ranking \n\nAlways Sunny in Philidelphia  23      "
                                      "\n\nHouse Hunters                 9       \n\nFixer Upper                   9       "
                                      "\n\nFresh Off the Boat            3       \n\nKilling Eve                   6       "
                                      "\n\nFuturama                      4       \n\nBrooklyn Nine Nine            4       "
                                      "\n\nKitchen Nightmares            4       \n\nHell's Kitchen                4       "
                                      "\n\nThe Bachelor                  3       \n\nShameless                     30      "
                                      "\n\nChopped                       55      \n\nCatfish                       40      "
                                      "\n\n911                           4       \n\nScream Queens                 4       "
                                      "\n\nThe Mindy Project             6       \n\nAmerican Horror Story         21      "
                                      "\n\nNew Girl                      4       \n\nParks and Recreation          1       "
                                      "\n\nBroad City                    35      \n\nForensic Files                1       "
                                      "\n\nJeapardy                      1       \n\nNailed It!                    2       "
                                      "\n\nBreaking Bad                  20      \n\nBlack Mirror                  2       "
                                      "\n\nYou                           2       \n\nBob's Burgers                 4       "
                                      "\n\nDear White People             2       \n\nQueer Eye                     2       "
                                      "\n\nAvatar the Last Airbender     19      \n\n"):
        passed = False
        print("failed search 22")

    if test_foo("search ranking <2") != ("Name                          Ranking \n\nParks and Recreation          1       "
                                         "\n\nForensic Files                1       \n\nJeapardy                      1       \n\n"):
        passed = False
        print("failed search 23")

    if test_foo("search ranking >50") != "Name                          Ranking \n\nChopped                       55      \n\n"\
                                        "\n\nAmerica's Next Top Model      67   \n\nClaws                         54  \n\n"\
                                        "\n\nVikings                       66   \n\nMan vs. Wild                  70 \n\n"\
                                        "\n\nMars                          71   \n\nImpractical Jokers            89 \n\n"\
                                        "\n\nProject Runway                77   \n\nDance Moms                    53 \n\n"\
                                        "\n\nThe Flintstones               102      \n\n":
        passed = False
        print("failed search 24")

    if test_foo("search ranking a") != "No results, check your query string\n":
        passed = False
        print("failed search 25")
    return passed

def test_status():
    passed = True
    if test_foo("status") != ("Invalid number of arguments.\nUsage:"
                  "\n\tstatus 'show' - returns the air status of any matching shows from your inputted string.\n"):
        passed = False
        print("Failed status 1")

    if test_foo("status house") != ("Your query 'house' returned one result:"
                                     "\n\t- House Hunters is on the air\n"):
        passed = False
        print("failed status 2")

    if test_foo("status z") != "No shows in database containing 'z'\n":
        passed = False
        print("failed status 3")


    return passed

def test_driver():
    passed = True
    if test_columns():
        print("Passed Columns")
    else:
        passed = False

    if test_exit():
        print("Passed Exit")
    else:
        passed = False

    if test_help():
        print("Passed Help")
    else:
        passed = False

    if test_network():
        print("Passed Network")
    else:
        passed = False

    if test_schema():
        print("Passed Schema")
    else:
        passed = False

    if test_seasons():
        print("Passed Seasons")
    else:
        passed = False

    if test_details():
        print("Passed Details")
    else:
        passed = False

    if test_genre():
        print("Passed Genre")
    else:
        passed = False

    if test_list():
        print("Passed List")
    else:
        passed = False

    if test_runtime():
        print("Passed Runtime")
    else:
        passed = False

    if test_search():
        print("Passed Search")
    else:
        passed = False

    if test_status():
        print("Passed Status")
    else:
        passed = False


    if passed:
        print("\nall tests passed")


if __name__ == '__main__':
    # TODO: replace this with our database once we have it
    database_name = "tv_tuner.db"
    # create a database connection
    test_cmd_shell.run_function()

        # test_cmd_shell.MainPrompt().default('a')
        # test_cmd_shell.MainPrompt().do_greet('x')
        # test_cmd_shell.MainPrompt().do_genre('house')
    test_driver()
