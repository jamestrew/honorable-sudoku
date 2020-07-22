import unittest
from puzzle import Puzzle
from resource import *


class WellFormed(object):

    @classmethod
    def testcases(cls):
        """ Fetch all test cases that abide to well-formed rules """
        return [
            cls.hard,
            cls.easy,
            cls.solved
        ]

    hard = [
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 3, 0, 8, 5,
        0, 0, 1, 0, 2, 0, 0, 0, 0,
        0, 0, 0, 5, 0, 7, 0, 0, 0,
        0, 0, 4, 0, 0, 0, 1, 0, 0,
        0, 9, 0, 0, 0, 0, 0, 0, 0,
        5, 0, 0, 0, 0, 0, 0, 7, 3,
        0, 0, 2, 0, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 4, 0, 0, 0, 9
    ]
    easy = [
        5, 0, 0, 8, 3, 2, 4, 0, 6,
        0, 6, 3, 7, 4, 0, 0, 0, 0,
        8, 0, 2, 1, 9, 0, 0, 0, 3,
        0, 3, 0, 0, 2, 9, 1, 0, 5,
        1, 0, 0, 0, 0, 8, 9, 6, 2,
        0, 0, 0, 5, 0, 0, 0, 7, 0,
        0, 0, 0, 0, 1, 0, 0, 2, 7,
        0, 2, 6, 0, 0, 0, 5, 0, 0,
        3, 1, 8, 0, 5, 0, 0, 4, 0
    ]
    solved = [
        1, 7, 2, 4, 8, 6, 5, 9, 3,
        8, 5, 6, 9, 3, 1, 7, 2, 4,
        3, 9, 4, 7, 5, 2, 1, 8, 6,
        7, 3, 5, 8, 2, 4, 6, 1, 9,
        9, 2, 1, 5, 6, 7, 3, 4, 8,
        4, 6, 8, 3, 1, 9, 2, 7, 5,
        6, 8, 9, 1, 7, 5, 4, 3, 2,
        2, 4, 7, 6, 9, 3, 8, 5, 1,
        5, 1, 3, 2, 4, 8, 9, 6, 7
    ]


class Pattern(object):

    @classmethod
    def testcases(cls):
        """ Fetch all test cases that form valid predictable compositions """
        return [
            cls.zero,
            cls.magic,
            cls.meso
        ]

    zero = [0]*(DIM*DIM)
    magic = [
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 2, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0
    ]
    meso = [
        0, 0, 0, 0, 0, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 0,
        0, 0, 1, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 1,
        0, 0, 0, 0, 0, 0, 1, 0, 0,
        0, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 1, 0, 0, 0, 0, 0
    ]


class Invalid(object):

    @classmethod
    def testcases(cls):
        """ Fetch all test cases break classical rules """
        return [
            cls.invalid1,
            cls.invalid2,
            cls.invalid3,
            cls.invalid4
        ]

    invalid1 = [
        1, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0
    ]
    invalid2 = [
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 1
    ]
    invalid3 = [
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0
    ]
    invalid4 = [
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 0, 0, 0, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0
    ]


class TestPuzzle(unittest.TestCase):

    __p = WellFormed.testcases() + Pattern.testcases()
    __p_invalid = Invalid.testcases()

    def test_validate(self):
        # Instantiation of invalid puzzle raises ValueError
        for p in self.__p_invalid:
            with self.assertRaises(ValueError):
                invalid = Puzzle(p)
                self.assertIsNone(invalid)
        # Validation of verified puzzles
        for p in self.__p:
            self.assertIsNotNone(Puzzle(p))

    def test_init(self):
        # Correct init_iteration of puzzle grid
        p1 = Puzzle(Pattern.zero)
        self.assertEqual(
            Pattern.zero,
            [p1.init_iterator for _ in range(DIM*DIM)]
        )
        # Only allow single scan for view initialization per instance
        self.assertRaises(StopIteration, lambda: p1.init_iterator)

        # Populated puzzle
        p2 = Puzzle(WellFormed.solved)
        self.assertEqual(
            WellFormed.solved,
            [p2.init_iterator for _ in range(DIM*DIM)]
        )
        self.assertRaises(StopIteration, lambda: p2.init_iterator)

    def test_properties(self):
        # empty puzzle is valid
        p = Puzzle(Pattern.zero)
        self.assertEqual(p.remaining_moves, DIM*DIM)
        self.assertTrue(p.empty)
        self.assertFalse(p.complete)

        # partial completeness
        p = Puzzle(WellFormed.easy)
        self.assertEqual(p.remaining_moves, 43)
        self.assertFalse(p.empty)
        self.assertFalse(p.complete)

        # complete/solved
        p = Puzzle(WellFormed.solved)
        self.assertEqual(p.remaining_moves, 0)
        self.assertFalse(p.empty)
        self.assertTrue(p.complete)

    def test_neighbor(self):
        p = Puzzle(WellFormed.solved)
        v_nbr = [
            [1, 8, 3, 7, 9, 4, 6, 2, 5],
            [7, 5, 9, 3, 2, 6, 8, 4, 1],
            [2, 6, 4, 5, 1, 8, 9, 7, 3],
            [4, 9, 7, 8, 5, 3, 1, 6, 2],
            [8, 3, 5, 2, 6, 1, 7, 9, 4],
            [6, 1, 2, 4, 7, 9, 5, 3, 8],
            [5, 7, 1, 6, 3, 2, 4, 8, 9],
            [9, 2, 8, 1, 4, 7, 3, 5, 6],
            [3, 4, 6, 9, 8, 5, 2, 1, 7]
        ]
        h_nbr = [
            [1, 7, 2, 4, 8, 6, 5, 9, 3],
            [8, 5, 6, 9, 3, 1, 7, 2, 4],
            [3, 9, 4, 7, 5, 2, 1, 8, 6],
            [7, 3, 5, 8, 2, 4, 6, 1, 9],
            [9, 2, 1, 5, 6, 7, 3, 4, 8],
            [4, 6, 8, 3, 1, 9, 2, 7, 5],
            [6, 8, 9, 1, 7, 5, 4, 3, 2],
            [2, 4, 7, 6, 9, 3, 8, 5, 1],
            [5, 1, 3, 2, 4, 8, 9, 6, 7]
        ]
        b_nbr = [
            [1, 7, 2, 8, 5, 6, 3, 9, 4],
            [4, 8, 6, 9, 3, 1, 7, 5, 2],
            [5, 9, 3, 7, 2, 4, 1, 8, 6],
            [7, 3, 5, 9, 2, 1, 4, 6, 8],
            [8, 2, 4, 5, 6, 7, 3, 1, 9],
            [6, 1, 9, 3, 4, 8, 2, 7, 5],
            [6, 8, 9, 2, 4, 7, 5, 1, 3],
            [1, 7, 5, 6, 9, 3, 2, 4, 8],
            [4, 3, 2, 8, 5, 1, 9, 6, 7]
        ]
        for i in range(DIM):
            self.assertEqual(v_nbr[i], p.neighbor(i, COL))
            self.assertEqual(h_nbr[i], p.neighbor(i, ROW))
            self.assertEqual(b_nbr[i], p.neighbor(i, BLK))

    def test_update(self):
        p = Puzzle(WellFormed.easy)
        prev_moves = p.remaining_moves

        # update state
        self.assertTrue(p.update(2, 1, 4))
        self.assertEqual(p.remaining_moves, prev_moves-1)
        self.assertFalse(p.empty)
        self.assertFalse(p.complete)
        self.assertEqual(p.neighbor(0)[7], 4)  # correct index updated
        self.assertTrue(p.update(2, 1, 0))     # revert update

        # top-left
        self.assertFalse(p.update(1, 0, 1))  # COL conflict
        self.assertFalse(p.update(0, 2, 4))  # ROW conflict
        self.assertFalse(p.update(2, 1, 5))  # BLK conflict
        self.assertEqual(p.neighbor(0)[3], 0)
        self.assertEqual(p.neighbor(0)[2], 0)
        self.assertEqual(p.neighbor(0)[7], 0)
        # bot-right
        self.assertFalse(p.update(7, 8, 3))  # COL conflict
        self.assertFalse(p.update(8, 6, 3))  # ROW conflict
        self.assertFalse(p.update(7, 7, 2))  # BLK conflict
        self.assertEqual(p.neighbor(8)[5], 0)
        self.assertEqual(p.neighbor(8)[6], 0)
        self.assertEqual(p.neighbor(8)[4], 0)
        # mid
        self.assertFalse(p.update(4, 4, 4))  # COL conflict
        self.assertFalse(p.update(5, 4, 7))  # ROW conflict
        self.assertFalse(p.update(5, 4, 8))  # BLK conflict
        self.assertEqual(p.neighbor(4)[4], 0)
        self.assertEqual(p.neighbor(4)[7], 0)
        self.assertEqual(p.neighbor(4)[7], 0)


if __name__ == "__main__":
    unittest.main()
