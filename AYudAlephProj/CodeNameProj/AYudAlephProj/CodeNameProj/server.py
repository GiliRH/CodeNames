import random
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import socket
import os
import threading

all_to_die = False  # global
IP = '0.0.0.0'
PORT = 6171


# --- Classes ----------------------------------------------------------------------
class Player:
    def __init__(self):
        pass


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


def get_words_list():
    """
    This function saves all the optional words for the game
    and saves them into a list
    """
    with open("words.txt", "r") as f:
        words_list = f.read()
        words_list = words_list.split()
    return words_list


def handle_client():
    pass


def handle_request():


def main(self):
    s = socket.socket()


if __name__ == '__main__':
    main()


# # --- FUNCTIONS --------------------------------------------------------------------
#
# #  diffie-Hellman
# def key_exchange(g, p, client):
#     # Server generates a private key
#     server_private_key = random.randint(1, p - 1)
#
#     # Server computes the public key and sends it to the client
#     server_public_key = pow(g, server_private_key, p)
#
#     # Send the public key to the client
#     client.send(str(server_public_key).encode())
#
#     # Receive the client's public key
#     client_public_key = int(client.recv(1024).decode())
#
#     # Server computes the shared secret key
#     server_shared_secret = pow(client_public_key, server_private_key, p)
#
#     # The shared secret key should now be the same as the client's
#     print("Shared secret key:", server_shared_secret)
#     return server_shared_secret
#
# ######################################################################################
# # Shared parameters
# p = 23
# g = 5
#
# # Create a socket object
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ip = '0.0.0.0'
# port = 12345
# s.bind((ip, port))
#
# # Wait for client connection
# s.listen(1)
# print("Waiting for client connection...")
# client, addr = s.accept()
# print("Client connected:", addr)
# ######################################################################################
#
# key = key_exchange(g, p, client)
#
# msg = client.recv(1024).decode()
# # cipher = AES.new(key, AES.MODE_ECB)
# # msg = unpad(cipher.dencrypt(msg),AES.block_size)
# print(msg)
# showinfo(
#         title='Information Recieved',
#         message=msg
#     )
#
#
# # Close the connection
# client.close()
