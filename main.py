#!/bin/usr/env python
import pygame
import pygame.mixer
from game import Game

def main():
    pygame.mixer.pre_init(44100, -16, 2, 800)
    pygame.init()
    clock = pygame.time.Clock()

    game = Game()
    while game.running:
        clock.tick(60)
        game.handle()
        game.tick()
        game.render()

if __name__ == '__main__':
    main()