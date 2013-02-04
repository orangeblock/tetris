import pygame
import resources
import menu
from state import State
from resources import load_image

class Score(State):
    def __init__(me, game, stats):
        me.stats = stats
        me.bg = load_image(resources.score_background, (game.w, game.h))

    def render(me, game):
        game.screen.blit(me.bg, (0,0))

        me.centerBlit(game, game.gameFont.render("Singles", 20, (255,255,255)), (game.w - game.w*2/3, game.h - game.h*10/12))
        me.centerBlit(game, game.gameFont.render("x" + str(me.stats.singles), 20, (255,255,255)), (game.w - game.w*1/3, game.h - game.h*10/12))
        me.centerBlit(game, game.gameFont.render("Doubles", 20, (255,255,255)), (game.w - game.w*2/3, game.h - game.h*9/12))
        me.centerBlit(game, game.gameFont.render("x" + str(me.stats.doubles), 20, (255,255,255)), (game.w - game.w*1/3, game.h - game.h*9/12))
        me.centerBlit(game, game.gameFont.render("Triples", 20, (255,255,255)), (game.w - game.w*2/3, game.h - game.h*8/12))
        me.centerBlit(game, game.gameFont.render("x" + str(me.stats.triples), 20, (255,255,255)), (game.w - game.w*1/3, game.h - game.h*8/12))
        me.centerBlit(game, game.gameFont.render("Tetris", 20, (255,255,255)), (game.w - game.w*2/3, game.h - game.h*7/12))
        me.centerBlit(game, game.gameFont.render("x" + str(me.stats.tetris), 20, (255,255,255)), (game.w - game.w*1/3, game.h - game.h*7/12))

        me.centerBlit(game, game.gameFont.render("Total Score", 20, (255,255,255)), (game.w/2, game.h-game.h*6/12))
        me.centerBlit(game, game.gameFont.render(str(me.stats.score), 20, (255,255,255)), (game.w/2, game.h-game.h*5/12))

        me.centerBlit(game, game.gameFont.render("Press Enter to continue", 20, (255,255,255)), (game.w/2, game.h-game.h*2/12))

    def tick(me, game):
        if any(game.eventkeys.values()):
            game.popState()
            me.changeState(game, menu.Menu(game))

    def centerBlit(me, game, surf, center):
        pos = surf.get_rect()
        pos.center = center
        game.screen.blit(surf, pos)
