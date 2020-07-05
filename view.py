from abc import ABCMeta, abstractmethod


class ViewMeta(type):

    def __init__(cls, name, base, attr_dict):
        if not(attr_dict.get("__metaclass__") is ViewMeta) and \
                (name in cls.views):
            cls.views[cls.views.index(name)] = cls
        super().__init__(name, base, attr_dict)


class MetaUnion(ABCMeta, ViewMeta): pass


class View(metaclass=MetaUnion):
    """ Sudoku::VIEW """
    # List of non-abstract views (fwd declaration)
    views = ["TextDisplay", "WidgetDisplay"]

    @abstractmethod
    def notify(self, x, y, val, /): pass


""" ( VIEW::.. ) """
from text_display import TextDisplay
from widget_display import WidgetDisplay
