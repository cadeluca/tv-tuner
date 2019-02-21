import sys
import tv_tuner
import io
import subprocess

# try:
#     import StringIO
# except ImportError:
#     from io import StringIO

# Debug variable
debug = True

# helper function to input a string through the command shell and get the console output
def test_foo(inp):
    captured_output = io.StringIO()  # Create StringIO object

    sys.stdout = captured_output  # and redirect stdout.
    tv_tuner.MainPrompt().onecmd(inp)
    sys.stdout = sys.__stdout__  # Reset redirect.
    # print 'Captured', captured_output.getvalue()  # Now works as before.

    return captured_output.getvalue()

# testing for exit
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
# testing for help
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

# testing for genre
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

# testing for network call
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

# testing for schema call
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

# testing for seasons call
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

# testing for tables call
def test_tables():
    passed = True
    # testing correct use of tables
    if test_foo("tables") != ("In database named tv_tuner, you have the following tables:\n\tnetworks\n\tshows\n"):
        passed = False
        print("failed tables 1")

    return passed
# testing for details calls
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
# testing for columns call
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
                                     "\n\tName\t\t\t\tType"
                                     "\n\t------\t\t\t\t------"
                                     "\n\tName                            varchar (40)"
                                     "\n\tRuntime                         integer"
                                     "\n\tSeasons                         integer"
                                     "\n\tStatus                          varchar (20)"
                                     "\n\tGenre                           varchar (20)"
                                     "\n\tNetworkID                       integer\n"):
        passed = False
        print("Failed Columns 2")
    # testin correct use networks
    if test_foo("columns networks") != ("The table 'networks' has the following columns:"
                                        "\n\tName\t\t\t\tType"
                                        "\n\t------\t\t\t\t------"
                                        "\n\tNetworkID                       integer"
                                        "\n\tNetwork                         varchar (20)"
                                        "\n\tRanking                         integer\n"):
        passed = False
        print("Failed Columns 3")
    #     testing columns caps
    if test_foo("columns Networks") != ("The table 'Networks' has the following columns:"
                                        "\n\tName\t\t\t\tType"
                                        "\n\t------\t\t\t\t------"
                                        "\n\tNetworkID                       integer"
                                        "\n\tNetwork                         varchar (20)"
                                        "\n\tRanking                         integer\n"):
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

    if test_foo("columns networks ranking") != ("23\n9\n3\n6\n4\n30\n55\n40\n21\n1\n35\n2\n20\n19\n10\n13\n34\n67\n11"
                                                "\n54\n66\n42\n70\n71\n89\n45\n77\n53\n24\n102\n"):
        passed = False
        print("Failed Column 7")

    if test_foo("columns shows name") != ("911\nAlways Sunny in Philidelphia\nAmerica's Next Top Model\n"
                                          "American Horror Story\nAvatar the Last Airbender\nBates Motel\n"
                                          "Big Brother\nBlack Mirror\nBob's Burgers\nBotched\nBreaking Bad\n"
                                          "Broad City\nBrooklyn Nine Nine\nCatfish\nChopped\nClaws\nDance Moms\n"
                                          "Dear White People\nFixer Upper\nForensic Files\nFresh Off the Boat\n"
                                          "Futurama\nHell's Kitchen\nHouse Hunters\nImpractical Jokers\nJeapardy\n"
                                          "Killing Eve\nKitchen Nightmares\nMan vs. Wild\nMars\nModern Family\n"
                                          "My 600 Pound Life\nNailed It!\nNew Girl\nParks and Recreation\n"
                                          "Project Runway\nQueer Eye\nRupaul's Drag Race\nScream Queens\nSesame Street\n"
                                          "Shameless\nThe Bachelor\nThe Flintstones\nThe Mindy Project\nVikings\nYou\n"):
        passed = False
        print("Failed coloumns 8")

    if test_foo("columns shows runtime") != ("30\n30\n60\n30\n60\n30\n30\n60\n60\n90\n60\n60\n60\n60\n60\n30\n60\n30\n"
                                             "30\n30\n30\n30\n45\n60\n60\n60\n30\n30\n50\n30\n60\n60\n60\n60\n30\n30\n"
                                             "60\n30\n60\n60\n30\n60\n60\n60\n60\n30\n"):
        passed = False
        print("failed columns 9")

    if test_foo("columns shows seasons") != ("12\n162\n5\n5\n1\n7\n6\n6\n18\n23\n10\n40\n7\n2\n2\n6\n8\n7\n8\n5\n11\n"
                                             "35\n2\n5\n4\n1\n9\n2\n2\n3\n5\n20\n5\n24\n49\n2\n5\n10\n5\n2\n8\n14\n17\n"
                                             "7\n7\n6\n"):
        passed = False
        print("failed columns 10")

    if test_foo("columns shows status") !=("On\nOn\nOff\nOn\nOn\nOff\nOn\nOff\nOn\nOn\nOn\nOn\nOff\nOn\nOff\nOff\nOn\n"
                                           "Off\nOff\nOn\nOff\nOn\nOn\nOff\nOn\nOn\nOn\nOn\nOn\nOff\nOff\nOn\nOn\nOn\n"
                                           "On\nOn\nOn\nOn\nOff\nOn\nOn\nOn\nOn\nOff\nOn\nOff\n"):
        passed = False
        print("failed columns 11")

    if test_foo("columns shows genre") != ("Comedy\nReality\nReality\nComedy\nThriller\nComedy\nComedy\nReality\n"
                                           "Competition\nReality\nDrama\nCompetition\nReality\nDrama\nThriller\n"
                                           "Comedy\nHorror\nComedy\nComedy\nComedy\nCrime\nGame show\nCompetition\n"
                                           "Drama\nHorror\nThriller\nComedy\nDrama\nReality\nComedy\nThriller\nReality\n"
                                           "Reality\nCompetition\nChildren's\nDrama\nDrama\nComedy\nReality\nEducational\n"
                                           "Comedy\nCompetition \nCompetition \nReality\nReality\nCartoon\n"):
        passed = False
        print("Failed columns 12")

    if test_foo("columns shows networkid") != ("1\n2\n2\n3\n4\n5\n5\n5\n5\n3\n6\n7\n8\n5\n5\n4\n9\n5\n10\n11\n10\n10\n"
                                               "12\n13\n12\n12\n5\n12\n12\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n"
                                               "25\n26\n27\n28\n29\n30\n"):
        passed = False
        print("failed columns 13")

    if test_foo("columns shows net") != "Encountered an error: no such column: net\n":
        passed = False
        print("failed columns 14")

    if test_foo("columns networks net") != "Encountered an error: no such column: net\n":
        passed = False
        print("failed columns 15")

    return passed

# testing for list calls
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
                                  "\n('Avatar the Last Airbender', 30, 3, 'Off', 'Comedy', 14)"
                                  "\n('Bates Motel', 60, 5, 'Off', 'Thriller', 15)"
                                  "\n('Big Brother', 60, 20, 'On', 'Reality', 16)"
                                  "\n('Botched', 60, 5, 'On', 'Reality', 17)"
                                  "\n(\"America's Next Top Model\", 60, 24, 'On', 'Competition', 18)"
                                  "\n('Sesame Street', 30, 49, 'On', \"Children's\", 19)"
                                  "\n('Claws', 30, 2, 'On', 'Drama', 20)"
                                  "\n('Vikings', 60, 5, 'On', 'Drama', 21)"
                                  "\n('Modern Family', 30, 10, 'On', 'Comedy', 22)"
                                  "\n('Man vs. Wild', 60, 5, 'Off', 'Reality', 23)"
                                  "\n('Mars', 60, 2, 'On', 'Educational', 24)"
                                  "\n('Impractical Jokers', 30, 8, 'On', 'Comedy', 25)"
                                  "\n(\"Rupaul's Drag Race\", 60, 14, 'On', 'Competition ', 26)"
                                  "\n('Project Runway', 60, 17, 'On', 'Competition ', 27)"
                                  "\n('Dance Moms', 60, 7, 'Off', 'Reality', 28)"
                                  "\n('My 600 Pound Life', 60, 7, 'On', 'Reality', 29)"
                                  "\n('The Flintstones', 30, 6, 'Off', 'Cartoon', 30)\n"):
        passed = False
        print("failed list 2")

    if test_foo("list networks") != ("['NetworkID', 'Network', 'Ranking']\n(1, 'FXX', 23)\n(2, 'HGTV', 9)"
                                     "\n(3, 'ABC', 3)\n(4, 'Hulu', 6)\n(5, 'Fox', 4)\n(6, 'Showtime', 30)"
                                     "\n(7, 'Food Network', 55)\n(8, 'MTV', 40)\n(9, 'FX', 21)\n(10, 'NBC', 1)"
                                     "\n(11, 'Comedy Central', 35)\n(12, 'Netflix', 2)\n(13, 'AMC', 20)"
                                     "\n(14, 'Nickolodean', 19)\n(15, 'A&E', 10)\n(16, 'CBS', 13)"
                                     "\n(17, 'E!', 34)\n(18, 'Oxygen', 67)\n(19, 'PBS', 11)\n(20, 'TNT', 54)"
                                     "\n(21, 'History Channel', 66)\n(22, 'USA', 42)\n(23, 'Discovery Channel', 70)"
                                     "\n(24, 'National Geographic', 71)\n(25, 'truTV', 89)\n(26, 'VH1', 45)\n"
                                     "(27, 'Bravo', 77)\n(28, 'Lifetime', 53)\n(29, 'TLC', 24)\n(30, 'Boomerang', 102)\n"):
        passed = False
        print("Failed list 3")

    if test_foo("list net") != "No matching table 'net'\n":
        passed = False
        print("Failed list 4")

    return passed

# testing for runtime calls
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

# testing for search calls
def test_search():
    passed = True
    if test_foo("search always") != "Name                          \n\nAlways Sunny in Philidelphia  \n\n":
        passed = False
        print("failed Search 1")

    if test_foo("search") != ("""Name                          

Always Sunny in Philidelphia  

House Hunters                 

Fixer Upper                   

Fresh Off the Boat            

Killing Eve                   

Futurama                      

Brooklyn Nine Nine            

Kitchen Nightmares            

Hell's Kitchen                

The Bachelor                  

Shameless                     

Chopped                       

Catfish                       

911                           

Scream Queens                 

The Mindy Project             

American Horror Story         

New Girl                      

Parks and Recreation          

Broad City                    

Forensic Files                

Jeapardy                      

Nailed It!                    

Breaking Bad                  

Black Mirror                  

You                           

Bob's Burgers                 

Dear White People             

Queer Eye                     

Avatar the Last Airbender     

Bates Motel                   

Big Brother                   

Botched                       

America's Next Top Model      

Sesame Street                 

Claws                         

Vikings                       

Modern Family                 

Man vs. Wild                  

Mars                          

Impractical Jokers            

Rupaul's Drag Race            

Project Runway                

Dance Moms                    

My 600 Pound Life             

The Flintstones               

"""):
        passed = False
        print("failed Search 2")

    if test_foo("search runtime") != ("""Name                          Runtime  

Always Sunny in Philidelphia  30       

House Hunters                 30       

Fixer Upper                   60       

Fresh Off the Boat            30       

Killing Eve                   60       

Futurama                      30       

Brooklyn Nine Nine            30       

Kitchen Nightmares            60       

Hell's Kitchen                60       

The Bachelor                  90       

Shameless                     60       

Chopped                       60       

Catfish                       60       

911                           60       

Scream Queens                 60       

The Mindy Project             30       

American Horror Story         60       

New Girl                      30       

Parks and Recreation          30       

Broad City                    30       

Forensic Files                30       

Jeapardy                      30       

Nailed It!                    45       

Breaking Bad                  60       

Black Mirror                  60       

You                           60       

Bob's Burgers                 30       

Dear White People             30       

Queer Eye                     50       

Avatar the Last Airbender     30       

Bates Motel                   60       

Big Brother                   60       

Botched                       60       

America's Next Top Model      60       

Sesame Street                 30       

Claws                         30       

Vikings                       60       

Modern Family                 30       

Man vs. Wild                  60       

Mars                          60       

Impractical Jokers            30       

Rupaul's Drag Race            60       

Project Runway                60       

Dance Moms                    60       

My 600 Pound Life             60       

The Flintstones               30       

"""):
        passed = False
        print("failed search 3")

    if test_foo("search runtime <31") != ("""Name                          Runtime  

Always Sunny in Philidelphia  30       

House Hunters                 30       

Fresh Off the Boat            30       

Futurama                      30       

Brooklyn Nine Nine            30       

The Mindy Project             30       

New Girl                      30       

Parks and Recreation          30       

Broad City                    30       

Forensic Files                30       

Jeapardy                      30       

Bob's Burgers                 30       

Dear White People             30       

Avatar the Last Airbender     30       

Sesame Street                 30       

Claws                         30       

Modern Family                 30       

Impractical Jokers            30       

The Flintstones               30       

"""):
        passed = False
        print("failed search 4")

    if test_foo("search runtime 50") != "Name                          Runtime  \n\nQueer Eye                     50       \n\n":
        passed = False
        print("failed search 5")

    if test_foo("search runtime >60") !="Name                          Runtime  \n\nThe Bachelor                  90       \n\n":
        passed = False
        print("failed search 6")

    if test_foo("search seasons") !=("""Name                          Seasons  

Always Sunny in Philidelphia  12       

House Hunters                 162      

Fixer Upper                   5        

Fresh Off the Boat            5        

Killing Eve                   1        

Futurama                      7        

Brooklyn Nine Nine            6        

Kitchen Nightmares            6        

Hell's Kitchen                18       

The Bachelor                  23       

Shameless                     10       

Chopped                       40       

Catfish                       7        

911                           2        

Scream Queens                 2        

The Mindy Project             6        

American Horror Story         8        

New Girl                      7        

Parks and Recreation          8        

Broad City                    5        

Forensic Files                11       

Jeapardy                      35       

Nailed It!                    2        

Breaking Bad                  5        

Black Mirror                  4        

You                           1        

Bob's Burgers                 9        

Dear White People             2        

Queer Eye                     2        

Avatar the Last Airbender     3        

Bates Motel                   5        

Big Brother                   20       

Botched                       5        

America's Next Top Model      24       

Sesame Street                 49       

Claws                         2        

Vikings                       5        

Modern Family                 10       

Man vs. Wild                  5        

Mars                          2        

Impractical Jokers            8        

Rupaul's Drag Race            14       

Project Runway                17       

Dance Moms                    7        

My 600 Pound Life             7        

The Flintstones               6        

"""):

        passed = False
        print("failed search 7")

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

    if test_foo("search status") != ("""Name                          Status  

Always Sunny in Philidelphia  On      

House Hunters                 On      

Fixer Upper                   Off     

Fresh Off the Boat            On      

Killing Eve                   On      

Futurama                      Off     

Brooklyn Nine Nine            On      

Kitchen Nightmares            Off     

Hell's Kitchen                On      

The Bachelor                  On      

Shameless                     On      

Chopped                       On      

Catfish                       Off     

911                           On      

Scream Queens                 Off     

The Mindy Project             Off     

American Horror Story         On      

New Girl                      Off     

Parks and Recreation          Off     

Broad City                    On      

Forensic Files                Off     

Jeapardy                      On      

Nailed It!                    On      

Breaking Bad                  Off     

Black Mirror                  On      

You                           On      

Bob's Burgers                 On      

Dear White People             On      

Queer Eye                     On      

Avatar the Last Airbender     Off     

Bates Motel                   Off     

Big Brother                   On      

Botched                       On      

America's Next Top Model      On      

Sesame Street                 On      

Claws                         On      

Vikings                       On      

Modern Family                 On      

Man vs. Wild                  Off     

Mars                          On      

Impractical Jokers            On      

Rupaul's Drag Race            On      

Project Runway                On      

Dance Moms                    Off     

My 600 Pound Life             On      

The Flintstones               Off     

"""):
        passed = False
        print("failed search 12")

    if test_foo("search status on") != ("""Name                          Status  

Always Sunny in Philidelphia  On      

House Hunters                 On      

Fresh Off the Boat            On      

Killing Eve                   On      

Brooklyn Nine Nine            On      

Hell's Kitchen                On      

The Bachelor                  On      

Shameless                     On      

Chopped                       On      

911                           On      

American Horror Story         On      

Broad City                    On      

Jeapardy                      On      

Nailed It!                    On      

Black Mirror                  On      

You                           On      

Bob's Burgers                 On      

Dear White People             On      

Queer Eye                     On      

Big Brother                   On      

Botched                       On      

America's Next Top Model      On      

Sesame Street                 On      

Claws                         On      

Vikings                       On      

Modern Family                 On      

Mars                          On      

Impractical Jokers            On      

Rupaul's Drag Race            On      

Project Runway                On      

My 600 Pound Life             On      

"""):
        passed = False
        print("failed search 13")

    if test_foo("search status off") != ("""Name                          Status  

Fixer Upper                   Off     

Futurama                      Off     

Kitchen Nightmares            Off     

Catfish                       Off     

Scream Queens                 Off     

The Mindy Project             Off     

New Girl                      Off     

Parks and Recreation          Off     

Forensic Files                Off     

Breaking Bad                  Off     

Avatar the Last Airbender     Off     

Bates Motel                   Off     

Man vs. Wild                  Off     

Dance Moms                    Off     

The Flintstones               Off     

"""):
        passed = False
        print("failed search 14")

    if test_foo("search status a") !=  "No results, check your query string\n":
        passed = False
        print("failed search 15")

    if test_foo("search genre") != ("""Name                          Genre   

Always Sunny in Philidelphia  Comedy  

House Hunters                 Reality 

Fixer Upper                   Reality 

Fresh Off the Boat            Comedy  

Killing Eve                   Thriller

Futurama                      Comedy  

Brooklyn Nine Nine            Comedy  

Kitchen Nightmares            Reality 

Hell's Kitchen                Competition

The Bachelor                  Reality 

Shameless                     Drama   

Chopped                       Competition

Catfish                       Reality 

911                           Drama   

Scream Queens                 Thriller

The Mindy Project             Comedy  

American Horror Story         Horror  

New Girl                      Comedy  

Parks and Recreation          Comedy  

Broad City                    Comedy  

Forensic Files                Crime   

Jeapardy                      Game show

Nailed It!                    Competition

Breaking Bad                  Drama   

Black Mirror                  Horror  

You                           Thriller

Bob's Burgers                 Comedy  

Dear White People             Drama   

Queer Eye                     Reality 

Avatar the Last Airbender     Comedy  

Bates Motel                   Thriller

Big Brother                   Reality 

Botched                       Reality 

America's Next Top Model      Competition

Sesame Street                 Children's

Claws                         Drama   

Vikings                       Drama   

Modern Family                 Comedy  

Man vs. Wild                  Reality 

Mars                          Educational

Impractical Jokers            Comedy  

Rupaul's Drag Race            Competition 

Project Runway                Competition 

Dance Moms                    Reality 

My 600 Pound Life             Reality 

The Flintstones               Cartoon 

"""):
        passed = False
        print("failed search 16")

    if test_foo("search genre game show") != "Name                          Genre   \n\nJeapardy                      Game show\n\n":
        passed = False
        print("Failed search 17")

    if test_foo("search genre q") != "No results, check your query string\n":
        passed = False
        print("failed search 18")

    if test_foo("search network") != ("""Name                          Network             

Always Sunny in Philidelphia  FXX                 

House Hunters                 HGTV                

Fixer Upper                   HGTV                

Fresh Off the Boat            ABC                 

Killing Eve                   Hulu                

Futurama                      Fox                 

Brooklyn Nine Nine            Fox                 

Kitchen Nightmares            Fox                 

Hell's Kitchen                Fox                 

The Bachelor                  ABC                 

Shameless                     Showtime            

Chopped                       Food Network        

Catfish                       MTV                 

911                           Fox                 

Scream Queens                 Fox                 

The Mindy Project             Hulu                

American Horror Story         FX                  

New Girl                      Fox                 

Parks and Recreation          NBC                 

Broad City                    Comedy Central      

Forensic Files                NBC                 

Jeapardy                      NBC                 

Nailed It!                    Netflix             

Breaking Bad                  AMC                 

Black Mirror                  Netflix             

You                           Netflix             

Bob's Burgers                 Fox                 

Dear White People             Netflix             

Queer Eye                     Netflix             

Avatar the Last Airbender     Nickolodean         

Bates Motel                   A&E                 

Big Brother                   CBS                 

Botched                       E!                  

America's Next Top Model      Oxygen              

Sesame Street                 PBS                 

Claws                         TNT                 

Vikings                       History Channel     

Modern Family                 USA                 

Man vs. Wild                  Discovery Channel   

Mars                          National Geographic 

Impractical Jokers            truTV               

Rupaul's Drag Race            VH1                 

Project Runway                Bravo               

Dance Moms                    Lifetime            

My 600 Pound Life             TLC                 

The Flintstones               Boomerang           

"""):
        passed = False
        print("failed search 19")

    if test_foo("search network food network") != ("""Name                          Network             

Chopped                       Food Network        

"""):
        passed = False
        print("failed search 20")

    if test_foo("search network q") != "No results, check your query string\n":
        passed = False
        print("failed search 21")

    if test_foo("search ranking") != ("""Name                          Ranking 

Always Sunny in Philidelphia  23      

House Hunters                 9       

Fixer Upper                   9       

Fresh Off the Boat            3       

Killing Eve                   6       

Futurama                      4       

Brooklyn Nine Nine            4       

Kitchen Nightmares            4       

Hell's Kitchen                4       

The Bachelor                  3       

Shameless                     30      

Chopped                       55      

Catfish                       40      

911                           4       

Scream Queens                 4       

The Mindy Project             6       

American Horror Story         21      

New Girl                      4       

Parks and Recreation          1       

Broad City                    35      

Forensic Files                1       

Jeapardy                      1       

Nailed It!                    2       

Breaking Bad                  20      

Black Mirror                  2       

You                           2       

Bob's Burgers                 4       

Dear White People             2       

Queer Eye                     2       

Avatar the Last Airbender     19      

Bates Motel                   10      

Big Brother                   13      

Botched                       34      

America's Next Top Model      67      

Sesame Street                 11      

Claws                         54      

Vikings                       66      

Modern Family                 42      

Man vs. Wild                  70      

Mars                          71      

Impractical Jokers            89      

Rupaul's Drag Race            45      

Project Runway                77      

Dance Moms                    53      

My 600 Pound Life             24      

The Flintstones               102     

"""):
        passed = False
        print("failed search 22")

    if test_foo("search ranking <2") != ("""Name                          Ranking 

Parks and Recreation          1       

Forensic Files                1       

Jeapardy                      1       

"""):
        passed = False
        print("failed search 23")

    if test_foo("search ranking >50") != """Name                          Ranking 

Chopped                       55      

America's Next Top Model      67      

Claws                         54      

Vikings                       66      

Man vs. Wild                  70      

Mars                          71      

Impractical Jokers            89      

Project Runway                77      

Dance Moms                    53      

The Flintstones               102     

""":
        passed = False
        print("failed search 24")

    if test_foo("search ranking a") != "No results, check your query string\n":
        passed = False
        print("failed search 25")
    return passed

# test for status calls
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
# test driver to call all different test categories
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


# main function to run the whole shindig
if __name__ == '__main__':
    database_name = "tv_tuner.db"
    # create a database connection
    tv_tuner.run_function()
    test_driver()
