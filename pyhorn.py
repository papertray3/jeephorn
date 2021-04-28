#! /bin/env python3

import logging
from decouple import config
import pygame.mixer
import gpiozero
import os
from signal import pause

BUTTONS = config('PYHORN_BUTTONS', cast=lambda v: [s.strip() for s in v.split(',')])
INTERFACE = config('PYHORN_INTERFACE')
STARTUP = config('PYHORN_STARTUP', default=None)
VOLUME = config('PYHORN_VOLUME', default=0.5, cast=float)

logging.basicConfig(level=logging.INFO)
logging.info(f'Using interface at {INTERFACE}')

#_MODE = 0o750

pygame.mixer.init()



## Make Interface (doesn't really need to be here)

# for button in BUTTONS:
#     path = os.path.join(INTERFACE, button)
#     os.makedirs(path, mode = _MODE, exist_ok=True)

# if STARTUP:
#     path = os.path.join(INTERFACE, STARTUP)
#     os.makedirs(path, mode=_MODE, exist_ok=True)

for blabel in BUTTONS:
    path = os.path.join(INTERFACE, blabel, blabel)
    logging.info(f'Matching button {blabel} with sound at {path}')
    sound = pygame.mixer.Sound(path)
    sound.set_volume(VOLUME)
    button = gpiozero.Button(blabel)
    button.when_pressed = sound.play

if STARTUP:
    path = os.path.join(INTERFACE, STARTUP, STARTUP)
    logging.info(f'Playing startup sound at {path}')
    startSound = pygame.mixer.Sound(path)
    startSound.set_volume(VOLUME)
    startSound.play()

pause()
    