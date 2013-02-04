import random
from shapes import shapes
from const import *

class Canvas:
    """
    This class contains the logic for the tetris game.
    It consists of a board(canvas) and an (anchor, shape) setup. Read on...

    The board is split in two. We have the canvas which is the logical part,
    containing 1s wherever there's a block and 0s everywhere else. Then we have
    the colormap that does basically the same, but instead of 0s we have -1s and instead
    of 1s we have an index (0 - 6) that represents each of the 7 shapes. This is used
    so that we can have different colors for each.
    *** Note: the board does NOT contain the current shape, only blocks already landed. ***

    The way the current shape is implemented is by using an (anchor, shape) setup.
    The anchor is basically an (x,y) coordinate of where we are currently on the board.
    The shape is the current shape. It is essentially being "drawn", starting from the anchor
    and extending to the right. Having this logical representation, we can then check for collisions
    and draw the shape (land it) when needed.
    """
    def __init__(me, rows, cols, startshape):
        me.rows, me.cols = me.dim = (rows, cols)
        me.canvas = [ [0] * cols for i in range(rows) ]
        me.colormap = [ [-1] * cols for i in range(rows) ]
        me.anchor = (0, cols/2)
        me.curr = startshape
        me.currcolor = shapes.index(startshape)

    def __getitem__(me, index):
        return me.colormap[index]
    
    def __setitem__(me, key, value):
        me.colormap[key] = value

    def rotate(me):
        """ 
        Rotates current piece (if possible).

        This method anticipates two scenarios - horizontal and vertical collision.
        Collision is considered either the wall or another shape already on the canvas.
        
        If a horizontal collision is encountered, it tries to continuously move to the left,
        until there's no collision. If that fails, returns without rotating.
        
        If a vertical collision is encountered it tries to continuously move up. Again, if that fails,
        return without rotating.
        """
        rotated = [ [row[i] for row in reversed(me.curr)] 
                    for i in range(len(me.curr[0])) ]

        a = me.anchor
        while not me.isValid(a, rotated):
            # if horizontal collision
            if a[1]+len(rotated[0])-1 >= me.cols \
            or 1 in [ me.canvas[a[0]][i] for i in range(a[1], a[1]+len(rotated[0])) ]:
                # check for validity of left move
                if me.canvas[a[0]][a[1]-1] == 1:
                    return
                # move left
                a = (a[0], a[1] - 1)
            else:
                # check for validity of going up
                if me.canvas[a[0]-1][a[1]] == 1:
                    return
                # move up
                a = (a[0] - 1, a[1])
        me.anchor = a
        me.curr = rotated

    def move(me, direct, shape = None):
        """ 
        Moves the given piece in the direction specified. If no piece given,
        moves current.

        Returns -1 if no move made, -2 if shape has touched another piece,
        and 1 if all went ok.
        """
        if not shape:
            shape = me.curr
        a = me.anchor

        if direct in [LEFT, RIGHT]:
            a = ( a[0], a[1] + direct )
        elif direct in [UP, DOWN]:
            a = ( a[0] + direct/2, a[1] )

        if not me.isValid(a, shape):
            if direct == DOWN:
                me.placeCurrent()
                return -2
            return -1
        me.anchor = a
        return 1
    
    def clearLines(me):
        """
        Clears all filled lines and returns a list of their indexes.
        """
        linesCleared = []
        for i in range(me.rows):
            if me.canvas[i] == [1]*me.cols:
                linesCleared.append(i)
                del me.canvas[i]
                del me.colormap[i]
                me.canvas.insert(0, [0]*me.cols)
                me.colormap.insert(0, [-1]*me.cols)
        return linesCleared

    def getBlocks(me, anch = None, shape = None):
        """
        Returns a list of tuples containing the positions of
        all the blocks for the given (anch, shape) setup.
        Defaults to the current if no arguments given.
        """
        if not shape:
            shape = me.curr
        if not anch:
            anch = me.anchor

        blocks = []
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == 1:
                    blocks.append( (anch[0]+i, anch[1]+j) )
        return blocks

    def placeCurrent(me):
        """ 
        Places current shape on the board.
        """
        for x, y in me.getBlocks():
            me.canvas[x][y] = 1
            me.colormap[x][y] = me.currcolor
        me.curr = None

    def reset(me, newshape):
        """
        Resets position and sets the new shape.
        If game is over (i.e. new shape is invalid) returns -1.
        """
        me.curr = newshape
        me.currcolor = shapes.index(newshape)
        me.anchor = (0, me.cols/2)
        if not me.isValid(me.anchor, me.curr):
            return -1

    def isValid(me, anch, shape):
        """
        Returns whether given (anch, shape) setup is valid.
        Meaning no touching other shapes or out of bounds.
        """
        for x, y in me.getBlocks(anch, shape):
            if x not in range(me.rows) or y not in range(me.cols) or me.canvas[x][y] == 1:
                return False
        return True
