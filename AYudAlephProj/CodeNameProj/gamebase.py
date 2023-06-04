# #from sympy import *
# import random
# import tkinter as tk
# from tkinter import ttk
# from tkinter.messagebox import showinfo
#
# class Card:
#     def __init__(self):
#         # 0 - neutral (should be 25-8-8-1 = 8): yellow
#         # 1 - blue (8): team color
#         # 2 - red (8): team color
#         # 3 - spy (1): black
#         self.known = 0
#         self.type = "AntiqueWhite2"
#         self.word = ""
#
# class Grid:
#     def __init__(self):
#         # 5x5
#         self.grid = [Card(), Card(), Card(), Card(), Card(),
#                      Card(), Card(), Card(), Card(), Card(),
#                      Card(), Card(), Card(), Card(), Card(),
#                      Card(), Card(), Card(), Card(), Card(),
#                      Card(), Card(), Card(), Card(), Card()]
#
#     def __str__(self):
#         st = "words:"
#         for c in self.grid:
#             st += c.word + ', '
#         st += '\ntypes:'
#         for t in self.grid:
#             st = st + str(t.type) + ','
#         return st
#
#     def set_board(self):
#         pos = []
#         for i in range(len(self.grid)):
#             pos.append(i)
#
#         for b in range(8): # blues
#             p = random.choice(pos)
#             self.grid[p].type = "sky blue"
#             pos.remove(p)
#
#         for r in range(8): # reds
#             p = random.choice(pos)
#             self.grid[p].type = "firebrick2"
#             pos.remove(p)
#
#         p = random.choice(pos) #spy
#         self.grid[p].type = "purple"
#         pos.remove(p)
#
#
#     def import_random_words(self):
#         words_list = get_words_list()
#         for i in range(len(self.grid)):
#             n = random.randint(0, len(words_list) -1)
#             self.grid[i].word = words_list[n]
#             words_list.remove(words_list[n])
#
#
#
#     def make_guess(self):
#         pass
#
#
# def get_words_list():
#     """
#     This function saves all the optional words for the game
#     and saves them into a list
#     """
#     with open("words.txt", "r") as f:
#         words_list = f.read()
#         words_list = words_list.split()
#     return words_list
#
# def return_clue_by_enter(enter_clue):
#     #self.config(state='disabled')
#     print(enter_clue.get())
#     return enter_clue.get()
#
#
# def create_root_leader(grid):
#     root = tk.Tk()
#     root.title('Grid')
#     root.config(bg='dark slate gray')
#
#     l = tk.Label(root, text="Enter Clue:")
#     l.grid(row=0, column=0, columnspan=1)
#
#     l.config(font=("Courier", 12))
#     enter_clue = tk.Entry(root, width=22)
#     enter_clue.grid(row=0, column=1, columnspan=3)
#     enter_clue.config(font=("Courier", 14))
#
#     btn = tk.Button(root, height=1, width=12, text="Enter", command=return_clue_by_enter(enter_clue))
#     btn.grid(row=0, column=4, columnspan=1)
#     for r in range(0, 5):
#         for c in range(0, 5):
#             b = tk.Button(root, text=grid.grid[5 * r + c].word, fg=grid.grid[5 * r + c].type, borderwidth=1, height=5,
#                           width=10)
#             b.grid(row=r+1, column=c, padx=2, pady=2)
#     root.mainloop()
#     return root
#
#
# def create_root_guesser(grid, clue):
#     root = tk.Tk()
#     root.title('Grid')
#     root.config(bg = 'dark slate gray')
#
#     l = tk.Label(root, text='Clue: ' + clue)
#     l.grid(row=0, column=0, columnspan=5)
#     l.config(font=("Courier", 14))
#
#     for r in range(0, 5):
#         for c in range(0, 5):
#             b = tk.Button(root, text=grid.grid[5 * r + c].word, bg='snow', borderwidth=1,height= 5, width=10)
#             b.grid(row=r+1, column=c, padx=2, pady=2)
#     root.mainloop()
#     return root
#
#
# def color_greed(grid , root):
#     for r in range(0, 5):
#         for c in range(0, 5):
#             tk.Button(root, borderwidth=1).grid(row=r, column=c).config(bg=grid.grid[5 * r + c].type)
#     root.mainloop()
#
#
#
# def main():
#     words_list = get_words_list()
#     grid = Grid()
#     grid.import_random_words()
#     grid.set_board()
#     print(grid)
#     root_leader = create_root_leader(grid)
#     root_guesser = create_root_guesser(grid, 'blablablaaaaa')
#
#     # color_greed(grid, root)
#
#
# if __name__ == "__main__":
#     main()
#
#
