#! /bin/env python3

import logging
from decouple import config
import pygame.mixer
import gpiozero
import os
from signal import pause

BUTTONS = config('PYHORN_BUTTONS', cast=lambda v: [s.strip() for s in v.split(',')])
ENABLE_SWITCH = config('PYHORN_ENABLE', default=None)
INTERFACE = config('PYHORN_INTERFACE')
STARTUP = config('PYHORN_STARTUP', default=None)
VOLUME = config('PYHORN_VOLUME', default=0.5, cast=float)

logging.basicConfig(level=logging.INFO)
logging.info(f'Using interface at {INTERFACE}')
if ENABLE_SWITCH:
    logging.info(f'Found enable switch at')
    enable = gpiozero.Button(ENABLE_SWITCH)
    enable.when_held = lambda: logging.info('System Enabled')
    enable.when_released = lambda: logging.info('System Disabled')
else:
    logging.info(f'No enable switch found')

pygame.mixer.init()

def testit():
    logging.info("Boom")

def getPath(label):
    return os.path.join(INTERFACE, label, label)

def getPlayFunc(path, sound):

    # Create funciton to check enable switch (could be lambda but eh)
    def playFunc():
        if (ENABLE_SWITCH and enable.is_active) or ENABLE_SWITCH == None:
            logging.info(f'Playing sound at: {path}')
            sound.play()
        else:
            logging.info(f'Sound requested for {path}, but system disabled')
    
    return playFunc

def createSound(path):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(VOLUME)
    return sound

def createButtonWithSound(button_label):
    path = getPath(button_label)
    logging.info(f'Matching label {button_label} with sound at {path}')
    sound = createSound(path)
    button = gpiozero.Button(button_label)

    button.when_pressed = getPlayFunc(path, sound)
    return button



for blabel in BUTTONS:
    button = createButtonWithSound(blabel)

if STARTUP:
    path = getPath(STARTUP)
    logging.info(f'Creating startup sound from {path}')
    startSound = getPlayFunc(path, createSound(path))
    startSound()
    

pause()
    