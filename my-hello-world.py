#!/usr/bin/env python

# Hello World in GIMP Python

from gimpfu import *

def hello_world(initstr, font, size, color) :
    # First do a quick sanity check on the font
    # Show the new image window
    # gimp.displays_flush()
    return 1/0

register(
    "python_fu_hello_world",
    "Hello world image",
    "Create a new image with your text string",
    "Akkana Peck",
    "Akkana Peck",
    "2010",
    "Hello world (Py) haha",
    "",      # Create a new image, don't work on an existing one
    [
        (PF_STRING, "string", "Text string", 'Hello, world!'),
        (PF_FONT, "font", "Font face", "Sans"),
        (PF_SPINNER, "size", "Font size", 50, (1, 3000, 1)),
        (PF_COLOR, "color", "Text color", (1.0, 0.0, 0.0))
    ],
    [],
    hello_world, menu="<Image>/File")

main()