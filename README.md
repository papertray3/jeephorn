# PY Horn
This is based off the project from [Mark Rober](https://www.youtube.com/watch?v=lv8wqnk_TsA). In this case, I'm using a Raspberry Pi 3+.

## Requirements:
* python3 - already installed on Raspbian
* gpiozero (pip) - already installed on Rasbian
* python-decouple (pip) - config stuff
* ~~sox - deb package~~
* pygame - already installed on Raspbian


## Notes

Tried using the pysox package to play sounds via Python, but found a massive delay. Perhaps that could be fixed but instead I use the Linux play command (sox)
and run that from the python script as a subprocess.

Might want to install apt-file during install

### General Idea
ENV vars that will capture:
* number of buttons
* location of sounds - should be /var/pihorn/sounds/<nameofsound>/{index.txt, <nameofsound>.<ext>}
  * index.txt - contains Human Readable name of sound (future expansion?)
  * the sound file itself
* location of button dir? - should be /var/pihorn/interface
  * Contains directories named after the button number; directory would contain a link to the sound and called


Use systemd to start up a simple Python script that would read those ENV vars and create the `button dir` and the various sub-directories.
Then create the Button objects (using gpiozero) and set the "pressed" method to a lambda function with the button ID as a parameter.

All lambda functions would call a defined function that would play (using a subprocess to call sox's `play` command). Probably need some kind of multi-button-pressing strategy to kill the current running sound before starting the new one. 


### Using pygame:

Think I'll just start with WAV files...but:

Example:
```
import pygame
file = 'some.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()
```

or

```
from gpiozero import Button
import pygame.mixer
from pygame.mixer import Sound
from signal import pause

pygame.mixer.init()

button_sounds = {
    Button(2): Sound("samples/drum_tom_mid_hard.wav"),
    Button(3): Sound("samples/drum_cymbal_open.wav"),
}

for button, sound in button_sounds.items():
    button.when_pressed = sound.play

pause()
```