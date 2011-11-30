"""
Helper functions created for the purpose of string formatting.
All functions accept a string, and return the same string surrounded
by the appropriate ascii color sequences for that function.

(The exception to this is _color(), which is only used in the
construction of the main functions.)
"""

COLOR_RESET = '\033[0m'

def _color(color):
    return lambda string: color + string + COLOR_RESET 

GREY = '\033[90m'
grey = _color(GREY)

RED = '\033[91m'
red = _color(RED)

GREEN = '\033[92m'
green = _color(GREEN)

YELLOW = '\033[93m'
yellow = _color(YELLOW)

BLUE = '\033[94m'
blue = _color(BLUE)

PINK = '\033[95m'
pink = _color(PINK)

VPINK = '\033[35m'
vpink = _color(VPINK)

CYAN = '\033[96m'
cyan = _color(CYAN)