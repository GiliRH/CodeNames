from random import randint
from sympy import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import socket
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random


port = 6171
root = tk.Tk()


# --- Classes ----------------------------------------------------------------------
class Card:
    def __init__(self):
        # 0 - neutral (should be 25-8-8-1 = 8): yellow
        # 1 - blue (8): team color
        # 2 - red (8): team color
        # 3 - spy (1): black
        self.known = 0
        self.type = "AntiqueWhite2"
        self.word = ""


class Board:
    def __init__(self):
        # 5x5
        self.role = ""
        self.team = ""
        self.board = [Card(), Card(), Card(), Card(), Card(),
                     Card(), Card(), Card(), Card(), Card(),
                     Card(), Card(), Card(), Card(), Card(),
                     Card(), Card(), Card(), Card(), Card(),
                     Card(), Card(), Card(), Card(), Card()]

    def __str__(self):
        st = "words:"
        for c in self.board:
            st += c.word + ', '
        st += '\ntypes:'
        for t in self.board:
            st = st + str(t.type) + ','
        return st

    def set_board(self):
        pos = []
        for i in range(len(self.board)):
            pos.append(i)

        for b in range(8): # blues
            p = random.choice(pos)
            self.board[p].type = "sky blue"
            pos.remove(p)

        for r in range(8): # reds
            p = random.choice(pos)
            self.board[p].type = "firebrick2"
            pos.remove(p)

        p = random.choice(pos) #spy
        self.board[p].type = "purple"
        pos.remove(p)

    def import_random_words(self):
        words_list = get_words_list()
        for i in range(len(self.board)):
            n = random.randint(0, len(words_list) - 1)
            self.board[i].word = words_list[n]
            words_list.remove(words_list[n])



# --- FUNCTIONS --------------------------------------------------------------------
# def login_clicked():
#     """ callback when the login button clicked
#     """
#     global s
#     msg = f'You entered email: {email.get()} and password: {password.get()}'
#     showinfo(
#         title='Information',
#         message=msg
#     )
#     print("email: ", email.get())
#     print("password: ", password.get())
#     # cipher = AES.new(key, AES.MODE_ECB)
#     # msg = cipher.encrypt(pad(msg,AES.block_size))
#     s.send(msg.encode())


def get_words_list():
    """
    This function saves all the optional words for the game
    and saves them into a list
    """
    with open("words.txt", "r") as f:
        words_list = f.read()
        words_list = words_list.split()
    return words_list


# def return_clue_by_enter(enter_clue):
#     # self.config(state='disabled')
#     print(enter_clue.get())
#     return enter_clue.get()


def create_root_leader(board):
    global root
    global enter_clue
    root.title('Grid')
    root.config(bg='dark slate gray')

    l = tk.Label(root, text="Enter Clue:")
    l.grid(row=0, column=0, columnspan=1)

    l.config(font=("Courier", 12))
    enter_clue = tk.Entry(root, width=22)
    enter_clue.grid(row=0, column=1, columnspan=3)
    enter_clue.config(font=("Courier", 14))

    btn = tk.Button(root, height=1, width=12, text="Enter", command=send_clue)
    btn.grid(row=0, column=4, columnspan=1)
    for r in range(0, 5):
        for c in range(0, 5):
            b = tk.Button(root, text=board.board[5 * r + c].word, fg=board.board[5 * r + c].type, borderwidth=1,
                          height=5,
                          width=10)
            b.grid(row=r + 1, column=c, padx=2, pady=2)
    root.mainloop()
    return root


def create_root_guesser(board, clue):
    global root
    root = tk.Tk()
    root.title('Grid')
    root.config(bg='dark slate gray')

    l = tk.Label(root, text='Clue: ' + clue)
    l.grid(row=0, column=0, columnspan=5)
    l.config(font=("Courier", 14))

    for r in range(0, 5):
        for c in range(0, 5):
            b = tk.Button(root, text=board.board[5 * r + c].word, bg='snow', borderwidth=1, height=5, width=10,
                          command=lambda r=r, c=c: send_guess(r, c, board))
            b.grid(row=r + 1, column=c, padx=2, pady=2)
    root.mainloop()
    return root


# def print_value(row, col):
#     print(find_in_grid(root, row, col).get())
#
#
# def find_in_grid(frame, row, column):
#     for children in frame.children.values():
#         info = children.grid_info()
#         #note that rows and column numbers are stored as string
#         if info['row'] == str(row) and info['column'] == str(column):
#             return btn
#     return None


def color_greed(grid, root):
    for r in range(0, 5):
        for c in range(0, 5):
            tk.Button(root, borderwidth=1).grid(row=r, column=c).config(bg=grid.grid[5 * r + c].type)
    root.mainloop()


def send_guess(row, col, board):
    print("row:", row, "col:", col, "--> text: ", board.board[5*row + col].word)


def send_clue():
    global clue
    clue = enter_clue.get()
    print("clue: ", clue)
    msg = "CLUE" + '~' + clue
    pass
    # !! send to server {msg}


def main():
    global clue
    words_list = get_words_list()
    board = Board()
    board.import_random_words()
    board.set_board()
    print(board)
    root_leader = create_root_leader(board)
    root_guesser = create_root_guesser(board, clue)


if __name__ == '__main__':
    main()




# #  diffie-Hellman
# def exchange_key(p,g,s):
#     # Receive the server's public key
#     server_public_key = int(s.recv(1024).decode())
#
#     # Client generates a private key
#     client_private_key = random.randint(1, p - 1)
#
#     # Client computes the public key and sends it to the server
#     client_public_key = pow(g, client_private_key, p)
#     s.send(str(client_public_key).encode())
#
#     # Client computes the shared secret key
#     client_shared_secret = pow(server_public_key, client_private_key, p)
#
#     # The shared secret key should now be the same as the server's
#     print("Shared secret key:", client_shared_secret)
#     return client_shared_secret

# ######################################################################################
# # Shared parameters
# p = 23
# g = 5
#
# # Create a socket object
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ip = '127.0.0.1'
# port = 12345
# s.connect((ip, port))
# ######################################################################################
#
# key = exchange_key(p, g, s)
#
# # # root window
# # root = tk.Tk()
# # root.geometry("300x150")
# # root.resizable(False, False)
# # root.title('Sign In')
# #
# # # store email address and password
# # email = tk.StringVar()
# # password = tk.StringVar()
# #
# # # Sign in frame
# # signin = ttk.Frame(root)
# # signin.pack(padx=10, pady=10, fill='x', expand=True)
# #
# # # email
# # email_label = ttk.Label(signin, text="Email Address:")
# # email_label.pack(fill='x', expand=True)
# #
# # email_entry = ttk.Entry(signin, textvariable=email)
# # email_entry.pack(fill='x', expand=True)
# # email_entry.focus()
# #
# # # password
# # password_label = ttk.Label(signin, text="Password:")
# # password_label.pack(fill='x', expand=True)
# #
# # password_entry = ttk.Entry(signin, textvariable=password, show="*")
# # password_entry.pack(fill='x', expand=True)
# #
# # # login button
# # login_button = ttk.Button(signin, text="Login", command=login_clicked)
# # login_button.pack(fill='x', expand=True, pady=10)
# #
# # root.mainloop()
#
# # Close the connection
# s.close()
