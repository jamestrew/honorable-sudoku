from resource import *

# ( TAG CONSTANTS )
NORMAL = 0
ORIGIN = 1
BADBIT = 2


class Cell(object):
    __value = 0
    __tag = BADBIT

    def __init__(self, value):
        if isinstance(value, Cell):
            self.__value = int(value)
            self.__tag = ORIGIN if value.locked else NORMAL
        elif isinstance(value, int):
            self.__value = value%(DIM+1)
            self.__tag = ORIGIN if value>0 else NORMAL

    # ( OVERRIDES ):
    def __lt__(self, other): return self.__value<other  # noqa
    def __gt__(self, other): return self.__value>other  # noqa
    def __le__(self, other): return self.__value<=other  # noqa
    def __ge__(self, other): return self.__value>=other  # noqa
    def __eq__(self, other): return self.__value==other  # noqa
    def __ne__(self, other): return self.__value!=other  # noqa

    def __mod__(self, other): return self.__value%other  # noqa
    def __int__(self): return self.__value  # noqa

    def __hash__(self):
        return hash(self.__value)

    def __str__(self): return f"{self.__value}"  # noqa

    def __repr__(self):
        lock = {NORMAL: "unlocked"}.get(self.__tag, "locked")
        return f"cell({self.__value}).{lock}"

    # METHODS ( PUBLIC ):
    def update(self, value):
        if self.__tag==ORIGIN: raise AttributeError(f"this cell is locked.")
        self.__value = value

    @property
    def locked(self):
        """ True if this cell is a part of the original puzzle, otherwise False. """
        return self.__tag == ORIGIN
