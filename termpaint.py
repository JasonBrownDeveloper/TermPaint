#!/bin/python3

import argparse
import csv

toolbox = {}
canvas = {}

# Box
parser = argparse.ArgumentParser( prog='Box', description='Draw a box' )
parser.add_argument( 'X', type=int )
parser.add_argument( 'Y', type=int )
parser.add_argument( 'Height', type=int )
parser.add_argument( 'Width', type=int )

def Box( args ):
    canvas.setdefault( args.Y, {} )[ args.X ] = '+'

    for i in range( 1, args.Width - 1 ):
        canvas[ args.Y ][ args.X + i ] = '-'

    canvas[ args.Y ][ args.X + args.Width - 1 ] = '+'

    for i in range( 1, args.Height - 1 ):
        canvas.setdefault( args.Y + i, {} )[ args.X ] = '|'
        canvas.setdefault( args.Y + i, {} )[ args.X + args.Width - 1 ] = '|'

    canvas.setdefault( args.Y + args.Height - 1, {} )[ args.X ] = '+'

    for i in range( 1, args.Width - 1 ):
        canvas[ args.Y + args.Height - 1 ][ args.X + i ] = '-'

    canvas[ args.Y + args.Height - 1 ][ args.X + args.Width - 1 ] = '+'

toolbox[ 'Box' ] = ( parser, Box )

# Table
parser = argparse.ArgumentParser( prog='Table', description='Draw a table' )
parser.add_argument( 'X', type=int )
parser.add_argument( 'Y', type=int )
parser.add_argument( 'row', nargs='*' )

def Table( args ):
    table = list( csv.reader( args.row ) )
    col_len = max( [ len( i ) for i in table ] )
    cell_len = max( [ len( j ) for i in table for j in i ] ) + 1

    for y, row in enumerate( table ):
        for x, column in enumerate( row ):
            canvas.setdefault( args.Y + ( y * 2 ), {} )[ args.X + ( x * cell_len ) ] = '+'
            for c in range( cell_len - 1 ):
                canvas[ args.Y + ( y * 2 ) ][ args.X + 1 + ( x * cell_len ) + c ] = '-'
        canvas[ args.Y + ( y * 2 ) ][ args.X + ( col_len * cell_len ) ] = '+'

        for x, column in enumerate( row ):
            canvas.setdefault( args.Y + ( y * 2 + 1 ), {} )[ args.X + ( x * cell_len ) ] = '|'
            for c in range( cell_len - 1 ):
                canvas[ args.Y + ( y * 2 + 1 ) ][ args.X + 1 + ( x * cell_len ) + c ] = column[ c ] if c < len( column ) else ' '
        canvas[ args.Y + ( y * 2 + 1 ) ][ args.X + ( col_len * cell_len ) ] = '|'

    for x in range( col_len ):
        canvas.setdefault( args.Y + ( len( table ) * 2 ), {} )[ args.X + ( x * cell_len ) ] = '+'
        for c in range( cell_len - 1 ):
            canvas[ args.Y + len( table ) * 2 ][ args.X + 1 + ( x * cell_len ) + c ] = '-'
    canvas[ args.Y + len( table ) * 2 ][ args.X + ( col_len * cell_len ) ] = '+'

toolbox[ 'Table' ] = ( parser, Table )
 
# Minkowski Line
parser = argparse.ArgumentParser( prog='MLine', description='Draw a Minkowski line' )
parser.add_argument( 'Sx', type=int )
parser.add_argument( 'Sy', type=int )
parser.add_argument( 'Ex', type=int )
parser.add_argument( 'Ey', type=int )

def MLine( args ):
    Sx, Ex = sorted( [ args.Sx, args.Ex ] )
    halfX = ( ( Ex - Sx ) // 2 )
    Sy, Ey = sorted( [ args.Sy, args.Ey ] )
    halfY = ( ( Ey - Sy ) // 2 )

    if halfX < halfY:
        canvas.setdefault( Sy, {} )[ Sx + halfX ] = '+'
        for i in range( halfX ):
            canvas[ Sy ][ Sx + i ] = '-'

        for i in range( 1, Ey - Sy ):
            canvas.setdefault( Sy + i, {} )[ Sx + halfX ] = '|'

        canvas.setdefault( Ey, {} )[ Sx + halfX ] = '+'
        for i in range( Ex - Sx - halfX ):
            canvas[ Ey ][ Sx + halfX + 1 + i ] = '-'

    else:
        for i in range( halfY ):
            canvas.setdefault( Sy + i, {} )[ Sx ] = '|'

        canvas.setdefault( Sy + halfY, {} )[ Sx ] = '+'

        for i in range( 1, Ex - Sx ):
            canvas[ Sy + halfY ][ Sx + i ] = '-'

        canvas[ Sy + halfY ][ Ex ] = '+'

        for i in range( Ey - Sy - halfY ):
            canvas.setdefault( Sy + halfY + 1 + i, {} )[ Ex ] = '|'

toolbox[ 'MLine' ] = ( parser, MLine )

# Bresenham Line
parser = argparse.ArgumentParser( prog='BLine', description='Draw a Bresenham line' )
parser.add_argument( 'Sx', type=int )
parser.add_argument( 'Sy', type=int )
parser.add_argument( 'Ex', type=int )
parser.add_argument( 'Ey', type=int )

def BLine( args ):
    dx = abs( args.Ex - args.Sx )
    sx = 1 if args.Sx < args.Ex else -1
    dy = -abs( args.Ey - args.Sy )
    sy = 1 if args.Sy < args.Ey else -1
    error = dx + dy
    
    x0, y0, x1, y1 = args.Sx, args.Sy, args.Ex, args.Ey
    while True:
        canvas.setdefault( y0, {} )[ x0 ] = 'L'
        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
                break

            error = error + dy
            x0 = x0 + sx

        if e2 <= dx:
            if y0 == y1:
                break

            error = error + dx
            y0 = y0 + sy

toolbox[ 'BLine' ] = ( parser, BLine )

# Circle
# https://www.computerenhance.com/p/efficient-dda-circle-outlines
parser = argparse.ArgumentParser( prog='Line', description='Draw a circle' )
parser.add_argument( 'Cx', type=int )
parser.add_argument( 'Cy', type=int )
parser.add_argument( 'R', type=int )

def Circle( args ):
    R2 = args.R + args.R

    X = args.R
    Y = 0
    dY = -2
    dX = R2 + R2 - 4
    D = R2 - 1

    while Y <= X:
        canvas.setdefault( args.Cy - Y, {} )[ args.Cx - X ] = 'a'
        canvas.setdefault( args.Cy - Y, {} )[ args.Cx + X ] = 'b'
        canvas.setdefault( args.Cy + Y, {} )[ args.Cx - X ] = 'c'
        canvas.setdefault( args.Cy + Y, {} )[ args.Cx + X ] = 'd'
        canvas.setdefault( args.Cy - X, {} )[ args.Cx - Y ] = 'e'
        canvas.setdefault( args.Cy - X, {} )[ args.Cx + Y ] = 'f'
        canvas.setdefault( args.Cy + X, {} )[ args.Cx - Y ] = 'g'
        canvas.setdefault( args.Cy + X, {} )[ args.Cx + Y ] = 'h'

        D += dY
        dY -= 4
        Y += 1

        if D < 0:
            D += dX
            dX -= 4
            X -= 1

toolbox[ 'Circle' ] = ( parser, Circle )

# Text
parser = argparse.ArgumentParser( prog='Line', description='Draw text' )
parser.add_argument( 'X', type=int )
parser.add_argument( 'Y', type=int )
parser.add_argument( 'text' )

def Text( args ):
    if args.text[ 0 ] in ( '"', "'" ):
        args.text = args.text[ 1:-1 ]

    for c in range( len( args.text ) ):
        canvas.setdefault( args.Y, {} )[ args.X + c ] = args.text[ c ]

toolbox[ 'Text' ] = ( parser, Text )
 
if __name__ == '__main__':
    import re

    parser = argparse.ArgumentParser( description='Draw primatives in the terminal' )
    parser.add_argument( 'shapes', nargs='+' )
    args = parser.parse_args()

    for shape in args.shapes:
        split = shape.split( ' ', 1 )
        primative, attributes = split + [''] * ( 2 - len( split ) ) 
        parser, painter = toolbox[ primative ]
        attributes = re.findall( "(?:\".*?\"|\S)+", attributes )
        args = parser.parse_args( attributes )
        painter( args )

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
