import pygame
import resources
from state import State
from gameplay import Gameplay
from resources import load_image
from pygame.locals import *

class Menu(State):
    def __init__(me, game, resume = 0):
        me.bg = load_image(resources.menu_background, (game.w, game.h))
        me.entries = [
            'New Game',
            'Options',
            'Exit'
        ]
        if resume:
            me.entries.insert(0, 'Resume')
        me.selected = 0

    def render(me, game):
        game.screen.blit(me.bg, (0,0))

        # blit main menu
        for i, opt in enumerate(me.entries):
            if i == me.selected:
                color = (255,255,255)
            else:
                color = (104,104,104)
            game.screen.blit(game.font.render(opt, 20, color), ((game.w-game.w/2-20), i*35+(game.h-game.h/2)))
       
    def tick(me, game):
        if game.eventkeys[K_DOWN]:
            me.selected = (me.selected + 1) % len(me.entries)
        if game.eventkeys[K_UP]:
            me.selected = (me.selected - 1) % len(me.entries)
        if game.eventkeys[K_ESCAPE]:
            # Leave Menu
            game.popState()
        if game.eventkeys[K_RETURN]:
            me.makeAction(game)

    def makeAction(me, game):
        """
        Applies the action based on the menu entry selected.
        """
        if len(me.entries) == 4:
            if me.selected == 0:
                # Resume Game
                game.popState()
                return
            else:
                me.selected -= 1

        if me.selected == 0:
            # New Game
            game.reset()
            me.changeState(game, Gameplay(game))
        elif me.selected == 1:
            # Options
            me.changeState(game, Options(game, me.bg))
        elif me.selected == 2:
            # Exit
            game.quit()

class Options(State):
    def __init__(me, game, background):
        me.bg = background
        me.entries = [
            ['Fullscreen' , ['Yes', 'No']]
        ]

        # vertical and horizontal selection for entries.
        me.vsel = 0
        me.hsel=[
            0 if game.fullscreen else 1,
        ]

    def render(me, game):
        game.screen.blit(me.bg, (0,0))
        
        for i, opt in enumerate(me.entries):
            if i == me.vsel:
                color = (255,255,255)
            else:
                color = (104,104,104)
            # blit the entry
            game.screen.blit(game.font.render(opt[0], 20, color), ((game.w-game.w/2-270), i*35+(game.h-game.h/2)))
            # blit its selected value
            game.screen.blit(game.font.render(str(me.entries[i][1][me.hsel[i]]), 20, color), ((game.w-game.w/2), i*35+(game.h-game.h/2)))

    def tick(me, game):
        if game.eventkeys[K_DOWN]:
            me.vsel = (me.vsel + 1) % len(me.entries)
        if game.eventkeys[K_UP]:
            me.vsel = (me.vsel - 1) % len(me.entries)
        if game.eventkeys[K_LEFT]:
            me.hsel[me.vsel] = (me.hsel[me.vsel] - 1) % len(me.entries[me.vsel][1])
            me.makeAction(game)
        if game.eventkeys[K_RIGHT]:
            me.hsel[me.vsel] = (me.hsel[me.vsel] + 1) % len(me.entries[me.vsel][1])
            me.makeAction(game)
        if game.eventkeys[K_ESCAPE]:
            game.popState()

    def makeAction(me, game):
        if me.vsel == 0:
            # toggle fullscreen
            if me.hsel[me.vsel] == 0:
                # on
                pygame.display.set_mode((game.w, game.h), FULLSCREEN)
                game.fullscreen = 1
            else:
                # off
                pygame.display.set_mode((game.w, game.h))
                game.fullscreen = 0