"""
BEFORE ANYONE SAYS THIS IS AI!
THIS IS NOT AI.
I MADE THIS IN ENGLISH CLASS YEARS AGO.
This is my own color module.
idc if you want to use it. go ahead.
"""

colors = ["\033[31m", "\033[38;2;255;165;0m", "\033[33m", "\033[32m", "\033[34m", "\033[35m"]
colorbackgrounds = ["\x1b[40m", "\x1b[41m", "\x1b[42m", "\x1b[43m", "\x1b[44m", "\x1b[45m", "\x1b[46m", "\x1b[47m"]

# Text Colors
CRed = colors[0]
COrange = colors[1]
CYellow = colors[2]
CGreen = colors[3]
CBlue = colors[4]
CPurple = colors[5]
CReset = "\033[0m"

#Background Colors
CBBlack = colorbackgrounds[0]
CBRed = colorbackgrounds[1]
CBGreen = colorbackgrounds[2]
CBYellow = colorbackgrounds[3]
CBBlue = colorbackgrounds[4]
CBPurple = colorbackgrounds[5]
CBCyan = colorbackgrounds[6]
CBWhite = colorbackgrounds[7]

#Custom Text Colors
def CColor(r, g, b):
    return f'\x1b[38;2;{r};{g};{b}m'


