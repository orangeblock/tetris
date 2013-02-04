import pygame

ingame_background = 'data/images/bg.png'
canvas_background = 'data/images/blockbg.png'
menu_background = 'data/images/menu.png'
score_background = 'data/images/score.png'

b_blue = 'data/images/blue.png'
b_teal = 'data/images/teal.png'
b_yellow = 'data/images/yellow.png'
b_brown = 'data/images/brown.png'
b_red = 'data/images/red.png'
b_green = 'data/images/green.png'
b_orange = 'data/images/orange.png'

sound_rot = 'data/audio/blop.wav'
sound_touch = 'data/audio/drop.wav'
sound_clear = 'data/audio/clear.wav'

font_menu = 'data/fonts/Bellerose.ttf'
font_game = 'data/fonts/Mouse_Deco.ttf'

def load_font(path, size = 30):
    return pygame.font.Font(path, size)

def load_sound(path, vol = 1.0):
    s = pygame.mixer.Sound(path)
    s.set_volume(vol)
    return s
    
def load_image(path, res = None):
    img = pygame.image.load(path).convert_alpha()
    if res:
        return pygame.transform.scale(img, res)
    return img