# Scyther

[![Travis](https://img.shields.io/travis/joshsamara/scyther.svg?maxAge=2592000?style=flat)](https://travis-ci.org/joshsamara/scyther)
[![Coveralls](https://img.shields.io/coveralls/joshsamara/scyther.svg?maxAge=2592000?style=flat)](https://coveralls.io/github/joshsamara/scyther)
[![Code Health](https://landscape.io/github/joshsamara/scyther/master/landscape.svg?style=flat)](https://landscape.io/github/joshsamara/scyther/master)

              ______
          _.-"______`._             ,.
        ,"_,"'      `-.`._         /.|
      ,',"   ____      `-.`.___   // |
      /.' ,-"'    `-._     `.   | j.  |  /|
    // .'   __...._  `"--.. `. ' |   | ' '
    j/  _.-"'       `._,."".   |  |   |/ '
    |.-'                    `.'/| |   | /
    '                        '/ | |   |/
                            /  ' '   '
                      |.   ` .'/.   /
                      | `. ,','.  ,'
                      |   \.' j.-'/
                      '   '   '. /
                      |          `"-...__
                      |             _..-'
                    ,|'      __.-7'   _......____
                    . |    ,"/   ,'`.'__........___`-...__
                    .    '-'_..' .-""-._         `""'-----`---...___
                    |____.-','" /      /`.._,"".                 _.-'
                  ,"`| ,'   '   |      .,--. ;--|             _,-"
                |   '.| `-.|   `.     ||   /   '`---.....--"'.
                '     `._  |     `+----`._;'.   `-..____..--'"
                  `.    | "'|__...-|,|       /     `.
                    |-..|`-.7    /   '      /   |  '|
                    ' |' `.||`--'    |      \   | . |
                            |        |       \  ' | |
                            `.      .'        .   ' '
                              `'-+-"|`.       '  ' /
                                |`-'  \     /  /.'
                                `   _ ,.   / ,'/
                                  ||'.'`.  / /,'
                                  `      ' .'
                                        /.' mh

(Art from http://www.fiikus.net/?pokedex)

The Pokemon catching simulator! Simulates Generation 1 capturing mechanics. Made
because I found catching Scyther in the safari zone interesting and thought it
would be cool to implement the mechanics myself.

# Compatibility

Written to work with `python==3.5+`.

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
