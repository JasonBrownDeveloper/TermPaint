# TermPaint

## Introduction

File this under, I can't believe something like this doesn't already
exist. This first release is a proof of concept that supports a
limited number of features. I have some idea of things I want to
support listed at the end of this document. Contributions and Pull
Requests are welcome.

## Use

This script draws primitives (e.g. Boxes, Lines, Circles, etc) with
font glyphs.

### Box

    $ ./termpaint.py 'Box -h'
    usage: Box [-h] X Y Height Width

    Draw a box

    positional arguments:
      X
      Y
      Height
      Width

    options:
      -h, --help  show this help message and exit


    $ ./termpaint.py 'Box 1 1 5 5'

     +---+
     |   |
     |   |
     |   |
     +---+

### Table

    $ ./termpaint.py 'Table -h'
    usage: Table [-h] X Y [row ...]

    Draw a table

    positional arguments:
      X
      Y
      row

    options:
      -h, --help  show this help message and exit

    $ ./termpaint.py 'Table 1 1 one,1,a," "  two,2,b," ," three,3,c,", "'

     +-----+-----+-----+-----+
     |one  |1    |a    |     |
     +-----+-----+-----+-----+
     |two  |2    |b    | ,   |
     +-----+-----+-----+-----+
     |three|3    |c    |,    |
     +-----+-----+-----+-----+

### Minkowski line

    $ ./termpaint.py 'MLine -h'
    usage: MLine [-h] Sx Sy Ex Ey

    Draw a Minkowski line

    positional arguments:
      Sx
      Sy
      Ex
      Ey

    options:
      -h, --help  show this help message and exit

    $ ./termpaint.py 'MLine 1 1 20 5'

     |
     |
     +------------------+
                        |
                        |

### Bresenham line

    $ ./termpaint.py 'BLine -h'
    usage: BLine [-h] Sx Sy Ex Ey

    Draw a Bresenham line

    positional arguments:
      Sx
      Sy
      Ex
      Ey

    options:
      -h, --help  show this help message and exit

    $ ./termpaint.py 'BLine 1 1 20 5'

     LLL
        LLLLL
             LLLL
                 LLLLL
                      LLL

### Circle

    $ ./termpaint.py 'Circle -h'
    usage: Line [-h] Cx Cy R

    Draw a circle

    positional arguments:
      Cx
      Cy
      R

    options:
      -h, --help  show this help message and exit

    $ ./termpaint.py 'Circle 6 6 5'

        eefff
       e     f
      a       b
     a         b
     a         b
     c         d
     c         d
     c         d
      c       d
       g     h
        gghhh

### Text

    $ ./termpaint.py 'Text -h'
    usage: Line [-h] X Y text

    Draw text

    positional arguments:
      X
      Y
      text

    options:
      -h, --help  show this help message and exit

    $ ./termpaint.py 'Text 1 1 "Hello World!"'

     Hello World!

### All Together

It's possible to provide multiple primitives in order to create
complex pictures.

    $ ./termpaint.py 'Box 1 1 5 5' 'Circle 12 12 2' 'MLine 3 3 12 12' 'BLine 3 12 12 3'

     +---+
     |   |
     | | |      L
     | | |     L
     +-|-+    L
       |     L
       +----L---+
           L    |
          L     |
         L     e|f
        L     a | b
       L      c | d
              c   d
               ghh

## Ideas for future improvements

* Unicode glyphs, particularly Box Drawings
* Ability to specify specific glyphs to use for different parts
* Read primitive instructions from stdin for piping
* An interactive mode with history/undo
* More primitives
