import pygame
import pygame.mixer
import menu
import resources
from const import *
from shapes import shapes
from canvas import Canvas
from pygame.locals import *

class Game:
    def __init__(me, title = "Tetris", res = (800, 600)):
        pygame.display.set_caption(title)
        me.screen = pygame.display.set_mode(res)
        me.w, me.h = res
        me.font = resources.load_font(resources.font_menu)
        me.gameFont = resources.load_font(resources.font_game)
        me.eventkeys = {
            K_LEFT : 0,
            K_RIGHT : 0,
            K_UP : 0,
            K_DOWN : 0,
            K_RETURN : 0,
            K_ESCAPE : 0,
        } # used for one tap events
        me.keymap = {
            K_DOWN : 0
        } # used for keys that can be held down
        me.sounds = {
            'ROT' : resources.load_sound(resources.sound_rot, 0.5),
            'TOUCH' : resources.load_sound(resources.sound_touch, 0.7),
            'CLEAR' : resources.load_sound(resources.sound_clear, 0.8)
        }
        me.fullscreen = 0
        me.running = True
        me.states = []
        me.pushState(menu.Menu(me))
        
    def render(me):
        me.states[-1].render(me)
        pygame.display.update()

    def handle(me):
        # reset the event maps
        for key in me.eventkeys:
            me.eventkeys[key] = 0
        for key in me.keymap:
            me.keymap[key] = 0

        # acquire new events
        for event in pygame.event.get():
            if event.type == QUIT:
                me.quit()
            elif event.type == KEYDOWN and event.key in me.eventkeys:
                me.eventkeys[event.key] = 1
        # and the held keys
        keystate = pygame.key.get_pressed()
        for key in me.keymap:
            if keystate[key]:
                me.keymap[key] = 1

    def tick(me):
        me.states[-1].tick(me)

    def pushState(me, state):
        me.states.append(state)

    def popState(me):
        del me.states[-1]

    def reset(me):
        me.states = []

    def quit(me):
        me.running = False