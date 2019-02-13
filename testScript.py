import StringIO
import sys
import test_cmd_shell
import unittest
import cli_animations


# Debug variable
debug = True


# TODO: ask Hibbeler if citations are necessary from SQLite official tutorial

if __name__ == '__main__':
    # TODO: replace this with our database once we have it
    database_name = "sample.db"
    # create a database connection
    conn = test_cmd_shell.create_connection('db/' + database_name)
    with conn:
        if debug:
            print("connected!")


        # test_cmd_shell.MainPrompt().default('a')
        # test_cmd_shell.MainPrompt().do_greet('x')


        def test_foo(inp):

            capturedOutput = StringIO.StringIO()  # Create StringIO object
            sys.stdout = capturedOutput  # and redirect stdout.
            test_cmd_shell.MainPrompt().onecmd(inp) # Call unchanged function.
            sys.stdout = sys.__stdout__  # Reset redirect.
            # print 'Captured', capturedOutput.getvalue()  # Now works as before.

            return capturedOutput.getvalue()


        def test_exit():
            passed = True
            if test_foo('q') != 'Bye\n':
                print "Failed exit 1"
                passed = False

            if test_foo('q') != 'Bye\n':
                print "Failed exit 2"
                passed = False

            if test_foo("exit") != 'Bye\n':
                print "Failed exit 3"
                passed = False

            return passed

        def test_driver():
            passed = True
            if test_exit():
                print "Passed Exit"
            else:
                passed = False

            if passed:
                print "all tests passed"

        test_driver()
