

class ConflictTask(object):
    def __init__(self, value, task, instance):
        self.__wdisplay = instance

        self.value = value
        self.task = task

    def __del__(self):
        self.__wdisplay.after_cancel(self.task)

    def __eq__(self, other): return self.value==other
    def __ne__(self, other): return self.value!=other

    def __hash__(self): return hash(self.value)


class ConflictTaskManager(object):
    """
    Sudoku::ConflictTaskManager
        Keeps track of the grid_update events to manage root.after() calls.
    """
    def __init__(self, instance):
        self.__wdisplay = instance
        self.__task_q = set()

    def __del__(self):
        for task in self.__task_q: del task

    def __contains__(self, item):
        return item in self.__task_q

    def add(self, value, task):
        self.__task_q.add(ConflictTask(value, task, self.__wdisplay))

    def remove(self, value):
        self.__task_q.remove(value)
