#from sympy import *
import random
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

class Card:
    def __init__(self):
        # 0 - neutral (should be 25-8-8-1 = 8): yellow
        # 1 - blue (8): team color
        # 2 - red (8): team color
        # 3 - spy (1): black
        self.known = 0
        self.type = "AntiqueWhite2"
        self.word = ""

class Grid:
    def __init__(self):
        # 5x5
        self.grid = [Card(), Card(), Card(), Card(), Card(),
                     Card(), Card(), Card(), Card(), Card(),
                     Card(), Card(), Card(), Card(), Card(),
                     Card(), Card(), Card(), Card(), Card(),
                     Card(), Card(), Card(), Card(), Card()]

    def __str__(self):
        st = "words:"
        for c in self.grid:
            st += c.word + ', '
        st += '\ntypes:'
        for t in self.grid:
            st = st + str(t.type) + ','
        return st

    def set_board(self):
        pos = []
        for i in range(len(self.grid)):
            pos.append(i)

        for b in range(8): # blues
            p = random.choice(pos)
            self.grid[p].type = "sky blue"
            pos.remove(p)

        for r in range(8): # reds
            p = random.choice(pos)
            self.grid[p].type = "firebrick2"
            pos.remove(p)

        p = random.choice(pos) #spy
        self.grid[p].type = "purple"
        pos.remove(p)


    def import_random_words(self):
        words_list = get_words_list()
        for i in range(len(self.grid)):
            n = random.randint(0, len(words_list) -1)
            self.grid[i].word = words_list[n]
            words_list.remove(words_list[n])



    def make_guess(self):
        pass


def get_words_list():
    """
    This function saves all the optional words for the game
    and saves them into a list
    """
    with open("words.txt", "r") as f:
        words_list = f.read()
        words_list = words_list.split()
    return words_list


def create_root(grid):
    root = tk.Tk()
    tk.Message(root, text="Enter Clue:").grid(row=0, column=1)
    enter = tk.Entry(root).grid(row=0, column=2)
    for r in range(0, 5):
        for c in range(0, 5):
            tk.Button(root, text=grid.grid[5 * r + c].word, bg=grid.grid[5 * r + c].type,
                      borderwidth=1).grid(row=r+1, column=c)
    root.mainloop()
    return root, enter


def color_greed(grid , root):
    for r in range(0, 5):
        for c in range(0, 5):
            tk.Button(root, borderwidth=1).grid(row=r, column=c).config(bg=grid.grid[5 * r + c].type)
    root.mainloop()



def main():
    words_list = get_words_list()
    grid = Grid()
    grid.import_random_words()
    grid.set_board()
    print(grid)
    root = create_root(grid)
    # color_greed(grid, root)


if __name__ == "__main__":
    main()


