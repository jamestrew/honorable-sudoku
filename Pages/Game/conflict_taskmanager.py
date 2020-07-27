

class ConflictTask(object):
    """
    Sudoku::ConflictTask
        A value-task pairing to prevent stacking of the de-highlight task.
    """
    def __init__(self, value:int, task, instance):
        self.__wdisplay = instance

        self.value = value  # cell value
        self.task = task    # de-highlight task

    def __del__(self):  # cancellation of de-highlighting tasks
        print(f"[Debug] \tCancelling {self.task}")
        self.__wdisplay.after_cancel(self.task)

    def __eq__(self, other): return self.value==other
    def __ne__(self, other): return self.value!=other

    def __hash__(self): return hash(self.value)


class ConflictTaskArray(object):
    """ Sudoku::ConflictTaskArray """
    def __init__(self, instance):
        self.__wdisplay = instance
        self.__task_q = set()  # set of unique tasks

    def __del__(self):  # cleanly cancel all pending tasks
        for task in self.__task_q: del task

    def __contains__(self, item):
        return item in self.__task_q

    def __len__(self):
        return len(self.__task_q)

    def add(self, value:int, task):
        """
        Pushes a task to de-highlight all conflicts resulting from an update
        to the given value.
        :param value: cell value
        :param task:  de-highlight task
        """
        print(f"[Debug] \tCreating task entry... ({value}: {task})")
        if value in self.__task_q:  # replace old de-highlight task
            self.__task_q.remove(value)
        self.__task_q.add(ConflictTask(value, task, self.__wdisplay))

    def remove(self, value:int):
        """
        Removes a task to de-highlight conflicts resulting from an update to
        the given value.
        :param value: cell value
        """
        self.__task_q.remove(value)


class ConflictTaskManager(object):
    """
    Sudoku::ConflictTaskManager
        Keeps track of the grid_update events to manage root.after() calls.
    """
    def __init__(self, instance):
        self.__wdisplay = instance
        self.__update_q = dict()  # TaskArray for each unique cell

    def __del__(self):  # cleanly destroy all update-queues
        for coord, q in self.__update_q.items(): del q

    def __contains__(self, item):
        return item in self.__update_q

    def __len__(self):
        return len(self.__update_q)

    def queue(self, x:int, y:int, value:int, task):
        locant = (x, y)
        print(f"[Debug] conflict_mgr.queue({x}, {y}, {value}, <>)")
        flag = False  # TEMP DEBUG VAR
        if not(locant in self.__update_q):
            self.__update_q[locant] = ConflictTaskArray(self.__wdisplay)
            flag = True
        print(f"[Debug] \tCreating locant entry... ({locant}: {value}: {task})\t\t{flag}")
        ct_arr = self.__update_q.get(locant)
        ct_arr.add(value, task)

    def dequeue(self, x:int, y:int, value:int):
        locant = (x, y)
        print(f"[Debug] conflict_mgr.dequeue({x}, {y}, {value}, <>)")
        ct_arr = self.__update_q.get(locant)
        ct_arr.remove(value)
        if len(ct_arr) == 0: del ct_arr, self.__update_q[locant]
