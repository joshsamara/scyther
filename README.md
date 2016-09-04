# Scyther

[![Travis](https://img.shields.io/travis/joshsamara/scyther.svg?maxAge=2592000?style=flat)](https://travis-ci.org/joshsamara/scyther)
[![Coveralls](https://img.shields.io/coveralls/joshsamara/scyther.svg?maxAge=2592000?style=flat)](https://coveralls.io/github/joshsamara/scyther)
[![Code Health](https://landscape.io/github/joshsamara/scyther/master/landscape.svg?style=flat)](https://landscape.io/github/joshsamara/scyther/master)

The Scyther catching simulator! Simulates Generation 1 capturing mechanics for
Scyther.

# Compatibility

Written to work with `python==3.4+`.

# Running Tests

I've included a separate requirements.txt file in the `tests` subdirectory. To
run tests, install these requirements and run

    $ nosetests --with-coverage

To run the tests with code coverage. To generate a coverage report, run

    $ coverage xml

after running these tests.

# Sources

This site has a great breakdown of the Gen 1 mechanics and how they work.

1. http://www.dragonflycave.com/mechanics/gen-i-capturing
2. http://www.dragonflycave.com/mechanics/gen-i-safari-zone
