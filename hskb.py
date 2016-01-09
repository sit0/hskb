#!/usr/bin/env python
from pymouse import PyMouse
from time import sleep
from functools import wraps
from keylistener import KeyListener

k = KeyListener()

WIDTH, HEIGHT = k.get_geometry()

CLICK_DELAY = 0.3

XY = {}
XY['end_turn'] = int(WIDTH * (HEIGHT / WIDTH < 0.75 and 0.8 or 0.92)), int(HEIGHT * 0.46)
XY['hero_power'] = int(WIDTH / 2 + WIDTH / 9), int(HEIGHT * 3 / 4)
XY['hero'] = WIDTH / 2, int(HEIGHT * 3 / 4)
XY['enemy'] = WIDTH / 2, int(HEIGHT / 6)
XY['play_btn'] = int(WIDTH * 5 / 6), int(HEIGHT * 5 / 6)

m = PyMouse()

def keep_mouse_position(mouse_moving_func):
    def _preserve(*args, **kwargs):
        _x, _y = m.position()
        mouse_moving_func(*args, **kwargs)
        m.move(_x, _y)
    return wraps(mouse_moving_func)(_preserve)

def click(what, btn=1, delay=CLICK_DELAY):
    m.click(XY[what][0], XY[what][1], btn)
    sleep(delay)

def click_position(x, y, btn=1, delay=CLICK_DELAY):
    m.click(x, y, btn)
    sleep(delay)

def use_hero_power():
    target_x, target_y = m.position()
    click('hero_power')
    click_position(target_x, target_y, 1)
    m.move(target_x, target_y)

@keep_mouse_position
def face_punch():
    click('hero')
    click('enemy')

def attack():
    target_x, target_y = m.position()
    click_position(target_x, target_y)
    click('enemy')
    m.move(target_x, target_y)

@keep_mouse_position
def end_turn():
    click('end_turn')

def draw_card():
    target_x, target_y = m.position()
    click_position(target_x, target_y)
    click_position(target_x, HEIGHT / 2)
    m.move(XY['hero'][0], XY['hero'][1])

@keep_mouse_position
def start_game():
    click('play_btn')

k.addKeyListener("L_CTRL+`", end_turn)
k.addKeyListener("L_CTRL+L_SHIFT", face_punch)
k.addKeyListener("L_CTRL+a", attack)
k.addKeyListener("L_CTRL+s", use_hero_power)
k.addKeyListener("`", draw_card)
k.addKeyListener("L_CTRL+SPACE", start_game)

print '^C to stop..'
try:
    k.start()
except:
    pass
