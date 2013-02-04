import pygame
import state
import random
import resources
import menu
import time
import score
from resources import load_image
from state import State
from canvas import Canvas
from shapes import shapes
from pygame.locals import *
from const import *

class Gameplay(State):
    def __init__(me, game):
        me.stats = Stats()
        me.nextShape = None
        me.rows, me.cols = 22, 10
        me.c = Canvas(me.rows, me.cols, me.genShape())
        me.wmarg = game.w * 25/100
        me.hmarg = game.h * 8/100
        me.bpx = min((game.w - 2*me.wmarg)/me.cols, (game.h - 2*me.hmarg)/me.rows) # block size

        # top left coordinate of the game canvas.
        me.xs = me.wmarg + (game.w - 2*me.wmarg)*35/100
        me.ys = me.hmarg + me.hmarg/3

        # resources
        me.bg = load_image(resources.ingame_background, (game.w, game.h))
        me.cbg = load_image(resources.canvas_background, (me.bpx, me.bpx))
        me.blockimgs = [
            load_image(resources.b_blue, (me.bpx, me.bpx)),
            load_image(resources.b_teal, (me.bpx, me.bpx)),
            load_image(resources.b_yellow, (me.bpx, me.bpx)),
            load_image(resources.b_brown, (me.bpx, me.bpx)),
            load_image(resources.b_red, (me.bpx, me.bpx)),
            load_image(resources.b_green, (me.bpx, me.bpx)),
            load_image(resources.b_orange, (me.bpx, me.bpx))
        ]

        me.delay = 250
        me.lastUpdate = pygame.time.get_ticks()

    def render(me, game):
        me.clearLines(game)

        # blit the background
        game.screen.blit(me.bg, (0,0))

        # blit next shape
        color = shapes.index(me.nextShape)
        for i, r in enumerate(me.nextShape):
            for j, b in enumerate(r):
                if me.nextShape[i][j] == 1:
                    game.screen.blit(me.blockimgs[color], ((me.wmarg+20)+j*me.bpx, me.hmarg+(i+5)*me.bpx))

        # blit lines/level
        game.screen.blit(game.gameFont.render("Level", 20, (255,255,255)), (me.wmarg, me.hmarg+14*me.bpx))
        game.screen.blit(game.gameFont.render(str(me.stats.level), 20, (255,255,255)), (me.wmarg, me.hmarg+16*me.bpx-me.bpx/2))
        game.screen.blit(game.gameFont.render("Lines", 20, (255,255,255)), (me.wmarg, me.hmarg+18*me.bpx))
        game.screen.blit(game.gameFont.render(str(me.stats.totalLines), 20, (255,255,255)), (me.wmarg, me.hmarg+20*me.bpx-me.bpx/2))

        # blit the canvas
        for i in range(me.rows):
            for j in range(me.cols):
                game.screen.blit(me.cbg, (me.xs+j*me.bpx, me.ys+i*me.bpx))
                color = me.c[i][j]
                if color != -1:
                    game.screen.blit(me.blockimgs[color], (me.xs+j*me.bpx, me.ys+i*me.bpx))

        # blit the current shape
        color = me.c.currcolor
        for r, c in me.c.getBlocks():
            game.screen.blit(me.blockimgs[color], (me.xs+c*me.bpx, me.ys+r*me.bpx))

    def clearLines(me, game):
        """
        Animates line clearing (if any complete lines exist).
        """
        if not me.stats.lines:
            return

        game.sounds['CLEAR'].play()
        for i in reversed(range(me.cols)):
            for j in me.stats.lines:
                game.screen.blit(me.cbg, (me.xs+i*me.bpx, me.ys+j*me.bpx))
            pygame.display.update()
            time.sleep(.03)
        me.stats.lines = []

    def tick(me, game):
        currtime = pygame.time.get_ticks()
        if game.eventkeys[K_DOWN] or currtime - me.lastUpdate > me.delay or game.keymap[K_DOWN]:
            if me.c.move(DOWN) == -2:
                game.sounds['TOUCH'].play()
                me.stats.update(me.c.clearLines())
                if me.c.reset(me.genShape()) == -1:
                    # Game Over
                    game.popState()
                    me.changeState(game, score.Score(game, me.stats))
            me.lastUpdate = currtime
        if game.eventkeys[K_LEFT]:
            me.c.move(LEFT)
        if game.eventkeys[K_RIGHT]:
            me.c.move(RIGHT)
        if game.eventkeys[K_UP]:
            game.sounds['ROT'].play()
            me.c.rotate()
        if game.eventkeys[K_ESCAPE]:
            me.changeState(game, menu.Menu(game, 1))

        if me.stats.level > 1:
            me.delay = 250 - 15 * me.stats.level-1

    def genShape(me):
        """
        Generates a random shape and returns it.
        Also sets the next shape.
        """
        if not me.nextShape:
            newshape = shapes[random.randint(0, len(shapes)-1)]
        else:
            newshape = me.nextShape
        me.nextShape = shapes[random.randint(0, len(shapes)-1)]
        return newshape

class Stats:
    def __init__(me):
        me.lines = []
        me.score = 0
        me.level = 1
        me.singles = 0
        me.doubles = 0
        me.triples = 0
        me.tetris  = 0
        me.totalLines = 0
        me.rewards = {
            1 : 100,
            2 : 400,
            3 : 1000,
            4 : 5000
        }

    def update(me, lines):
        if not lines:
            return

        me.lines = lines
        me.totalLines += len(lines)

        if len(lines) == 1:
            me.singles += 1
        elif len(lines) == 2:
            me.doubles += 1
        elif len(lines) == 3:
            me.triples += 1
        elif len(lines) == 4:
            me.tetris += 1

        me.score += me.rewards[len(lines)] * me.level

        if me.totalLines >= me.level * 10:
            me.level += 1