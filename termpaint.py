#!/bin/python3

import argparse
import csv

toolbox = {}
canvas = {}
glyphs = {
      'unicode' : {
          'Horizontal' : '─'
        , 'Vertical' : '│'
        , 'Down and Right' : '┌'
        , 'Down and Left' : '┐'
        , 'Up and Right' : '└'
        , 'Up and Left' : '┘'
        , 'Vertical and Right' : '├'
        , 'Vertical and Left' : '┤'
        , 'Horizontal and Down' : '┬'
        , 'Horizontal and Up' : '┴'
        , 'Vertical and Horizontal' : '┼'
        , 'Diagonal Right Left' : '╱'
        , 'Diagonal Left Right' : '╲'
        , 'Diagonal Cross' : '╳' }

    , 'ascii' : {
          'Horizontal' : '-'
        , 'Vertical' : '|'
        , 'Down and Right' : '+'
        , 'Down and Left' : '+'
        , 'Up and Right' : '+'
        , 'Up and Left' : '+'
        , 'Vertical and Right' : '+'
        , 'Vertical and Left' : '+'
        , 'Horizontal and Down' : '+'
        , 'Horizontal and Up' : '+'
        , 'Vertical and Horizontal' : '+'
        , 'Diagonal Right Left' : '/'
        , 'Diagonal Left Right' : '\\'
        , 'Diagonal Cross' : 'X' } }

# Box
parser = argparse.ArgumentParser( prog='Box', description='Draw a box' )
parser.add_argument( 'X', type=int )
parser.add_argument( 'Y', type=int )
parser.add_argument( 'Height', type=int )
parser.add_argument( 'Width', type=int )

def Box( args, attributes ):
    g = glyphs[ args.glyphs ]

    canvas.setdefault( attributes.Y, {} )[ attributes.X ] = g[ 'Down and Right' ]

    for i in range( 1, attributes.Width - 1 ):
        canvas[ attributes.Y ][ attributes.X + i ] = g[ 'Horizontal' ]

    canvas[ attributes.Y ][ attributes.X + attributes.Width - 1 ] = g[ 'Down and Left' ]

    for i in range( 1, attributes.Height - 1 ):
        canvas.setdefault( attributes.Y + i, {} )[ attributes.X ] = g[ 'Vertical' ]
        canvas.setdefault( attributes.Y + i, {} )[ attributes.X + attributes.Width - 1 ] = g[ 'Vertical' ]

    canvas.setdefault( attributes.Y + attributes.Height - 1, {} )[ attributes.X ] = g[ 'Up and Right' ]

    for i in range( 1, attributes.Width - 1 ):
        canvas[ attributes.Y + attributes.Height - 1 ][ attributes.X + i ] = g[ 'Horizontal' ]

    canvas[ attributes.Y + attributes.Height - 1 ][ attributes.X + attributes.Width - 1 ] = g[ 'Up and Left' ]

toolbox[ 'Box' ] = ( parser, Box )

# Table
parser = argparse.ArgumentParser( prog='Table', description='Draw a table' )
parser.add_argument( 'X', type=int )
parser.add_argument( 'Y', type=int )
parser.add_argument( 'row', nargs='*' )

def Table( args, attributes ):
    g = glyphs[ args.glyphs ]

    table = list( csv.reader( attributes.row ) )
    col_len = max( [ len( i ) for i in table ] )
    cell_len = max( [ len( j ) for i in table for j in i ] ) + 1

    for y, row in enumerate( table ):
        for x, column in enumerate( row ):
            if y == 0 and x == 0:
                canvas.setdefault( attributes.Y + ( y * 2 ), {} )[ attributes.X + ( x * cell_len ) ] = g[ 'Down and Right' ]
            elif y == 0:
                canvas.setdefault( attributes.Y + ( y * 2 ), {} )[ attributes.X + ( x * cell_len ) ] = g[ 'Horizontal and Down' ]
            elif x == 0:
                canvas.setdefault( attributes.Y + ( y * 2 ), {} )[ attributes.X + ( x * cell_len ) ] = g[ 'Vertical and Right' ]
            else:
                canvas.setdefault( attributes.Y + ( y * 2 ), {} )[ attributes.X + ( x * cell_len ) ] = g[ 'Vertical and Horizontal' ]

            for c in range( cell_len - 1 ):
                canvas[ attributes.Y + ( y * 2 ) ][ attributes.X + 1 + ( x * cell_len ) + c ] = g[ 'Horizontal' ]

        if y == 0:
            canvas[ attributes.Y + ( y * 2 ) ][ attributes.X + ( col_len * cell_len ) ] = g[ 'Down and Left' ]
        else:
            canvas[ attributes.Y + ( y * 2 ) ][ attributes.X + ( col_len * cell_len ) ] = g[ 'Vertical and Left' ]

        for x, column in enumerate( row ):
            canvas.setdefault( attributes.Y + ( y * 2 + 1 ), {} )[ attributes.X + ( x * cell_len ) ] = g[ 'Vertical' ]
            for c in range( cell_len - 1 ):
                canvas[ attributes.Y + ( y * 2 + 1 ) ][ attributes.X + 1 + ( x * cell_len ) + c ] = column[ c ] if c < len( column ) else ' '

        canvas[ attributes.Y + ( y * 2 + 1 ) ][ attributes.X + ( col_len * cell_len ) ] = g[ 'Vertical' ]

    for x in range( col_len ):
        if x == 0:
            canvas.setdefault( attributes.Y + ( len( table ) * 2 ), {} )[ attributes.X + ( x * cell_len ) ] = g[ 'Up and Right' ]
        else:
            canvas.setdefault( attributes.Y + ( len( table ) * 2 ), {} )[ attributes.X + ( x * cell_len ) ] = g[ 'Horizontal and Up' ]

        for c in range( cell_len - 1 ):
            canvas[ attributes.Y + len( table ) * 2 ][ attributes.X + 1 + ( x * cell_len ) + c ] = g[ 'Horizontal' ]

    canvas[ attributes.Y + len( table ) * 2 ][ attributes.X + ( col_len * cell_len ) ] = g[ 'Up and Left' ]

toolbox[ 'Table' ] = ( parser, Table )

# Minkowski Line
parser = argparse.ArgumentParser( prog='MLine', description='Draw a Minkowski line' )
parser.add_argument( 'Sx', type=int )
parser.add_argument( 'Sy', type=int )
parser.add_argument( 'Ex', type=int )
parser.add_argument( 'Ey', type=int )

def MLine( args, attributes ):
    g = glyphs[ args.glyphs ]

    Sx, Ex = sorted( [ attributes.Sx, attributes.Ex ] )
    halfX = ( ( Ex - Sx ) // 2 )
    Sy, Ey = sorted( [ attributes.Sy, attributes.Ey ] )
    halfY = ( ( Ey - Sy ) // 2 )

    if halfX < halfY:
        canvas.setdefault( Sy, {} )[ Sx + halfX ] = g[ 'Down and Left' ]
        for i in range( halfX ):
            canvas[ Sy ][ Sx + i ] = g[ 'Horizontal' ]

        for i in range( 1, Ey - Sy ):
            canvas.setdefault( Sy + i, {} )[ Sx + halfX ] = g[ 'Vertical' ]

        canvas.setdefault( Ey, {} )[ Sx + halfX ] = g[ 'Up and Right' ]
        for i in range( Ex - Sx - halfX ):
            canvas[ Ey ][ Sx + halfX + 1 + i ] = g[ 'Horizontal' ]

    else:
        for i in range( halfY ):
            canvas.setdefault( Sy + i, {} )[ Sx ] = g[ 'Vertical' ]

        canvas.setdefault( Sy + halfY, {} )[ Sx ] = g[ 'Up and Right' ]

        for i in range( 1, Ex - Sx ):
            canvas[ Sy + halfY ][ Sx + i ] = g[ 'Horizontal' ]

        canvas[ Sy + halfY ][ Ex ] = g[ 'Down and Left' ]

        for i in range( Ey - Sy - halfY ):
            canvas.setdefault( Sy + halfY + 1 + i, {} )[ Ex ] = g[ 'Vertical' ]

toolbox[ 'MLine' ] = ( parser, MLine )

# Bresenham Line
parser = argparse.ArgumentParser( prog='BLine', description='Draw a Bresenham line' )
parser.add_argument( 'Sx', type=int )
parser.add_argument( 'Sy', type=int )
parser.add_argument( 'Ex', type=int )
parser.add_argument( 'Ey', type=int )

def BLine( args, attributes ):
    g = glyphs[ args.glyphs ]

    dx = abs( attributes.Ex - attributes.Sx )
    sx = 1 if attributes.Sx < attributes.Ex else -1
    dy = -abs( attributes.Ey - attributes.Sy )
    sy = 1 if attributes.Sy < attributes.Ey else -1
    error = dx + dy

    char = {
          True : {
               1 : ( g[ 'Horizontal' ], g[ 'Up and Right' ], g[ 'Down and Left' ] )
            , -1 : ( g[ 'Horizontal' ], g[ 'Up and Left' ], g[ 'Down and Right' ] ) }
        , False : {
               1 : ( g[ 'Vertical' ], g[ 'Down and Left' ], g[ 'Up and Right' ] )
            , -1 : ( g[ 'Vertical' ], g[ 'Down and Right' ], g[ 'Up and Left' ] ) }
        }[ -dy < dx ][ sx ]

    x0, y0, x1, y1 = attributes.Sx, attributes.Sy, attributes.Ex, attributes.Ey
    while True:
        canvas.setdefault( y0, {} )[ x0 ] = char[ 0 ]

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
                break

            if -dy > dx:
                canvas.setdefault( y0, {} )[ x0 + sx ] = char[ 1 ]
                canvas.setdefault( y0, {} )[ x0 ] = char[ 2 ]
            error = error + dy
            x0 = x0 + sx

        if e2 <= dx:
            if y0 == y1:
                break

            if -dy < dx:
                canvas.setdefault( y0 + sy, {} )[ x0 - sx ] = char[ 1 ]
                canvas.setdefault( y0, {} )[ x0 - sx ] = char[ 2 ]
            error = error + dx
            y0 = y0 + sy

toolbox[ 'BLine' ] = ( parser, BLine )

# Circle
# https://www.computerenhance.com/p/efficient-dda-circle-outlines
parser = argparse.ArgumentParser( prog='Circle', description='Draw a circle' )
parser.add_argument( 'Cx', type=int )
parser.add_argument( 'Cy', type=int )
parser.add_argument( 'R', type=int )

def Circle( args, attributes ):
    g = glyphs[ args.glyphs ]

    R2 = attributes.R + attributes.R

    X = attributes.R
    Y = 0
    dY = -2
    dX = R2 + R2 - 4
    D = R2 - 1

    while Y <= X:
        canvas.setdefault( attributes.Cy - Y, {} )[ attributes.Cx - X ] = g[ 'Vertical' ]
        canvas.setdefault( attributes.Cy - Y, {} )[ attributes.Cx + X ] = g[ 'Vertical' ]
        canvas.setdefault( attributes.Cy + Y, {} )[ attributes.Cx - X ] = g[ 'Vertical' ]
        canvas.setdefault( attributes.Cy + Y, {} )[ attributes.Cx + X ] = g[ 'Vertical' ]
        canvas.setdefault( attributes.Cy - X, {} )[ attributes.Cx - Y ] = g[ 'Horizontal' ]
        canvas.setdefault( attributes.Cy - X, {} )[ attributes.Cx + Y ] = g[ 'Horizontal' ]
        canvas.setdefault( attributes.Cy + X, {} )[ attributes.Cx - Y ] = g[ 'Horizontal' ]
        canvas.setdefault( attributes.Cy + X, {} )[ attributes.Cx + Y ] = g[ 'Horizontal' ]

        D += dY
        dY -= 4
        Y += 1

        if D < 0:
            canvas.setdefault( attributes.Cy - Y + 1, {} )[ attributes.Cx - X ] = g[ 'Down and Right' ]
            canvas.setdefault( attributes.Cy - Y + 1, {} )[ attributes.Cx - X + 1] = g[ 'Up and Left' ]
            canvas.setdefault( attributes.Cy - Y + 1, {} )[ attributes.Cx + X ] = g[ 'Down and Left' ]
            canvas.setdefault( attributes.Cy - Y + 1, {} )[ attributes.Cx + X - 1] = g[ 'Up and Right' ]
            canvas.setdefault( attributes.Cy + Y - 1, {} )[ attributes.Cx - X + 1 ] = g[ 'Down and Left' ]
            canvas.setdefault( attributes.Cy + Y - 1, {} )[ attributes.Cx - X ] = g[ 'Up and Right' ]
            canvas.setdefault( attributes.Cy + Y - 1, {} )[ attributes.Cx + X - 1 ] = g[ 'Down and Right' ]
            canvas.setdefault( attributes.Cy + Y - 1, {} )[ attributes.Cx + X ] = g[ 'Up and Left' ]
            canvas.setdefault( attributes.Cy - X, {} )[ attributes.Cx - Y + 1 ] = g[ 'Down and Right' ]
            canvas.setdefault( attributes.Cy - X + 1, {} )[ attributes.Cx - Y + 1 ] = g[ 'Up and Left' ]
            canvas.setdefault( attributes.Cy - X, {} )[ attributes.Cx + Y - 1 ] = g[ 'Down and Left' ]
            canvas.setdefault( attributes.Cy - X + 1, {} )[ attributes.Cx + Y - 1 ] = g[ 'Up and Right' ]
            canvas.setdefault( attributes.Cy + X, {} )[ attributes.Cx - Y + 1 ] = g[ 'Up and Right' ]
            canvas.setdefault( attributes.Cy + X - 1, {} )[ attributes.Cx - Y + 1 ] = g[ 'Down and Left' ]
            canvas.setdefault( attributes.Cy + X, {} )[ attributes.Cx + Y - 1 ] = g[ 'Up and Left' ]
            canvas.setdefault( attributes.Cy + X - 1, {} )[ attributes.Cx + Y - 1 ] = g[ 'Down and Right' ]
            D += dX
            dX -= 4
            X -= 1

toolbox[ 'Circle' ] = ( parser, Circle )

# Text
parser = argparse.ArgumentParser( prog='Text', description='Draw text' )
parser.add_argument( 'X', type=int )
parser.add_argument( 'Y', type=int )
parser.add_argument( 'text' )

def Text( args, attributes ):
    if attributes.text[ 0 ] in ( '"', "'" ):
        attributes.text = attributes.text[ 1:-1 ]

    for c in range( len( attributes.text ) ):
        canvas.setdefault( attributes.Y, {} )[ attributes.X + c ] = attributes.text[ c ]

toolbox[ 'Text' ] = ( parser, Text )

if __name__ == '__main__':
    import re

    parser = argparse.ArgumentParser( description='Draw primatives in the terminal' )
    parser.add_argument( '-g', '--glyphs', choices=[ 'unicode', 'ascii' ], default='unicode' )
    parser.add_argument( 'shapes', nargs='+' )
    args = parser.parse_args()

    for shape in args.shapes:
        split = shape.split( ' ', 1 )
        primative, attributes = split + [''] * ( 2 - len( split ) )
        parser, painter = toolbox[ primative ]
        attributes = re.findall( "(?:\".*?\"|\S)+", attributes )
        attributes = parser.parse_args( attributes )
        painter( args, attributes )

    for y in range( max( canvas.keys() ) + 1 ):
        if y not in canvas:
            print()
        else:
            l = canvas[ y ]
            width = max( l.keys() ) + 1
            plot = [ ' ' ] * width
            for p, c in sorted( l.items() ):
                plot[ p ] = c

            print( ''.join( plot ) )
