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
    captured_output = io.BytesIO()  # Create StringIO object

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
    if test_foo('help') !="\nDocumented commands (type help <topic>):\n========================================\ncolumns  exit   help  network  schema  seasons  tables\ndetails  genre  list  runtime  search  status \n\n":
        print("Failed help 1")
        passed = False

    if test_foo('?') !="\nDocumented commands (type help <topic>):\n========================================\ncolumns  exit   help  network  schema  seasons  tables\ndetails  genre  list  runtime  search  status \n\n":
        print("Failed help 2")
        passed = False

    if test_foo('help exit') != 'Exits the application. Shorthand: \'x\' \'q\' \'Ctrl-D\'.\n':
        print("Failed help exit")
        passed = False

    return passed


def test_genre():
    passed = True
    if test_foo("genre house") !="Your query 'house' returned one result:\n\t- House Hunters is a Reality show\n":
        passed = False
        print("Failed genre 1")
    if test_foo('genre') !=("Invalid number of arguments.\nUsage:"
                  "\n\tgenre 'show' - returns the genre of any matching shows from your inputted string.\n"):
        passed = False
        print("Failed genre 2")
    if test_foo('genre hosu') != "No shows in database containing 'hosu'\n":
        passed = False
        print("failed genre 3")
    #
    return passed


def test_driver():
    passed = True
    if test_funtions():
        print("Passed functions")
    if test_exit():
        print("Passed Exit")
    if test_help():
        print("Passed Help")
    else:
        passed = False

    
    if passed:
        print("all tests passed")


if __name__ == '__main__':
    # TODO: replace this with our database once we have it
    database_name = "tv_tuner.db"
    # create a database connection
    test_cmd_shell.mainFunction()

        # test_cmd_shell.MainPrompt().default('a')
        # test_cmd_shell.MainPrompt().do_greet('x')
        # test_cmd_shell.MainPrompt().do_genre('house')
    test_driver()
