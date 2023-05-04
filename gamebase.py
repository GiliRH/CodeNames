from sympy import *
import random
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


class LeaderGrid:
    def __init__(self):
        self.enemy_guessed = 0
        self.left2guess = 0
        # in the grid:
        # 0 - regular (should be 25-8-8-1 = 8)
        # 1 - own (8)
        # 2 - enemy (8)
        # 3 - spy (1)
        self.grid = [0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0]

        self.words = ["", "", "", "", "",
                      "", "", "", "", "",
                      "", "", "", "", "",
                      "", "", "", "", "",
                      "", "", "", "", ""]

    def set_board(self):
        pass



class GuesserGrid:
    def __init__(self):
        # in the grid:
        # 0 - regular (should be 25-8-8-1 = 8)
        # 1 - own (8)
        # 2 - enemy (8)
        # 3 - spy (1)
        # 4 - unknown
        self.grid = [4, 4, 4, 4, 4,
                     4, 4, 4, 4, 4,
                     4, 4, 4, 4, 4,
                     4, 4, 4, 4, 4,
                     4, 4, 4, 4, 4]
        self.words = ["", "", "", "", "",
                      "", "", "", "", "",
                      "", "", "", "", "",
                      "", "", "", "", "",
                      "", "", "", "", ""]

    def set_board(self):
        pass

    def make_guess(self):
        pass


def get_words_list():
    pass


def import_random_words():
    pass


