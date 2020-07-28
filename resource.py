import numpy as np


""" PUZZLE CONSTANTS """

DIM = 9  # N, where the sudoku model (Puzzle) is an N*N matrix
SUB = 3  # the dimension of puzzle box/block

# Enumerated neighbor look-up codes
BLK = 0  # box/block
COL = 1  # column
ROW = 2  # row

# MainMenu options
PLAY = 0
LOAD = 1
SETT = 2
HELP = 3
EXIT = 4

# GameConfiguration settings
USER_PLAY = 0  # human
COMP_PLAY = 1  # computer

EASY_DIFF = 0  # easy
HARD_DIFF = 1  # hard
MAGI_DIFF = 2  # magic

X,Y = 0, 1  # Vector2 index enumerated
W,H = 0, 1

PAD_THIC = 5
PAD_THIN = 0.5

# ( colors )
def s_rgb(color:str) -> tuple:  # noqa: E302
    """
    Given a color-code in hex, converted into RGB.
    :param color: code in hex
    :return: the RGB-vector
    """
    return tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

def s_hex(color:tuple) -> str:  # noqa: E302
    """
    Given a color-code in RGB, converted into a hex-string.
    :param color: code in RGB
    :return: the hex-string
    """
    return "#%02x%02x%02x"%color

def color_shift(color:tuple, offset:tuple) -> str:  # noqa: E302
    return s_hex(tuple(np.subtract(color, offset)))


# ( colors - theme )
WHITE = "#FFFFFF"
CHAMPAGNE_PINK = "#EACDC2"
POPSTAR = "#B75D69"
TWILIGHT_LAVENDER = "#774C60"
OFFSET_LAVENDER = color_shift(s_rgb(TWILIGHT_LAVENDER), (18, 18, 18))
DARK_PURPLE = "#372549"
XIKETIC = "#1A1423"
BLACK = "#000000"

# ( fonts )
FONT_FAMILY = "Courier"
H1 = (FONT_FAMILY, "38", "bold")
H2 = (FONT_FAMILY, "26", "bold")
H3 = (FONT_FAMILY, "22", "bold")

P = (FONT_FAMILY, "12", "normal")
P_SELECT = (FONT_FAMILY, "12", "bold")
P_VAL = (FONT_FAMILY, "16", "bold")

# ( widgets - cascading style )
MENU_TITLE = {
    "bg": TWILIGHT_LAVENDER,
    "fg": CHAMPAGNE_PINK,
    "font": H1
}
SUBMENU_TITLE = {
    "bg": TWILIGHT_LAVENDER,
    "fg": CHAMPAGNE_PINK,
    "font": H2
}
PAGE_TITLE = {
    "bg": TWILIGHT_LAVENDER,
    "fg": CHAMPAGNE_PINK,
    "font": H3
}
FOOT_TOOLTIP = {
    "bg": TWILIGHT_LAVENDER,
    "fg": CHAMPAGNE_PINK,
    "font": P,
    "justify": "left"
}
ROOT = {
    "bg": XIKETIC
}
TRANSPARENT = {
    "bg": TWILIGHT_LAVENDER
}
GRP_INTERACT = {
    "bg": TWILIGHT_LAVENDER,
    "highlightbackground": CHAMPAGNE_PINK,
    "highlightthickness": 6
}
GRP_FEEDBACK = GRP_INTERACT
CMD_CENTER = {
    "bg": TWILIGHT_LAVENDER,
    "fg": CHAMPAGNE_PINK,
    "font": (FONT_FAMILY, "16", "normal"),
    "relief": "flat"
}
CMD_UPDATE = {
    "bg": OFFSET_LAVENDER,
    "fg": CHAMPAGNE_PINK,
    "font": (FONT_FAMILY, "12", "normal"),
    "relief": "flat"
}
CMD_HOVER_ACTIVE = {
    "bg": POPSTAR,
    "fg": DARK_PURPLE
}
CMD_HOVER_INACTIVE = {
    "bg": TWILIGHT_LAVENDER,
    "fg": CHAMPAGNE_PINK
}
TBL_HDR = {
    "bg": TWILIGHT_LAVENDER,
    "fg": CHAMPAGNE_PINK,
    "font": P
}
TBL_DEFAULT_CVAL = {
    "bg": TWILIGHT_LAVENDER,
    "fg": CHAMPAGNE_PINK,
    "font": P_SELECT
}
NAV_BAR = {
    "bg": TWILIGHT_LAVENDER,
    "fg": CHAMPAGNE_PINK,
    "font": (FONT_FAMILY, "11", "normal")
}
CELL_BG = {
    "bg": CHAMPAGNE_PINK,
    "width": 38,
    "height": 38
}
CELL_FG = {
    "bg": CHAMPAGNE_PINK,
    "fg": XIKETIC,
    "font": P_VAL
}
CELL_FG_LOCK = {
    "bg": CHAMPAGNE_PINK,
    "fg": TWILIGHT_LAVENDER,
    "font": P_VAL
}
CELL_SELECT = {
    "bg": "#C6EFCE",
    "width": 38,
    "height": 38
}
# ( widgets - markup )
G_MENU_INTERACT = {
    "padx": 240,
    "pady": (12, 6)
}
G_MENU_FEEDBACK = {
    "padx": 240,
    "pady": (6, 12)
}
P_FILL = {
    "expand": True,
    "fill": "both"
}
NUM_BG = {
    "bg": CHAMPAGNE_PINK,
    "width": 60,
    "height": 60
}
NUM_FG = {
    "bg": CHAMPAGNE_PINK,
    "fg": XIKETIC,
    "font": H3
}
CNT_BG = {
    "bg": CHAMPAGNE_PINK,
    "width": 25,
    "height": 25
}
CNT_FG = {
    "bg": CHAMPAGNE_PINK,
    "fg": TWILIGHT_LAVENDER,
    "font": P
}
