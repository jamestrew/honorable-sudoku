

class ConflictTask(object):
    """
    Sudoku::ConflictTask
        A value-task pairing to prevent stacking of the de-highlight task.
    """
    def __init__(self, value:int, task, instance):
        self.__wdisplay = instance

        self.value = value  # cell value
        self.task = task    # de-highlight task

    def __del__(self):
        # cancellation of de-highlighting root.after() task
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
        self.__task_q = set()   # set of unique tasks

    def __del__(self):
        # cleanly cancel all pending tasks
        for task in self.__task_q: del task

    def __contains__(self, item):
        return item in self.__task_q

    def add(self, value:int, task):
        """
        Pushes a task to de-highlight all conflicts resulting from an update
        to the given value.
        :param value: cell value
        :param task:  de-highlight task
        """
        self.__task_q.add(ConflictTask(value, task, self.__wdisplay))

    def remove(self, value:int):
        """
        Removes a task to de-highlight conflicts resulting from an update to
        the given value.
        :param value: cell value
        """
        self.__task_q.remove(value)
