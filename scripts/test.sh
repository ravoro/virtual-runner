#!/bin/bash
# The script takes 2 possible sets of values:
#     1) Specific module, class or method (based on: https://docs.python.org/3/library/unittest.html#command-line-interface)
#     2) Specific package (requires use of additional "discover" argument) (based on: https://docs.python.org/3/library/unittest.html#test-discovery)
#
# Examples:
#     * Execute a test method:  "./test.sh tests.controllers.test_home.TestHome.test_redirect"
#     *        ...alternative:  "./test.sh tests/controllers/test_home/TestHome/test_redirect.py"
#     * Execute a test class:   "./test.sh tests.controllers.test_home.TestHome"
#     * Execute a test module:  "./test.sh tests.controllers.test_home"
#     * Execute a test package: "./test.sh discover tests.controllers" (note the additional discover argument)
#
# Default functionality:
#     Execute all tests within the "tests" package (i.e. "./test.sh" will ultimately run "./test.sh discover tests")


EXEC_TESTS="discover tests"
if [ "$#" -ne 0 ]; then
    EXEC_TESTS="$@"
fi

source venv/bin/activate

python -m unittest ${EXEC_TESTS}
