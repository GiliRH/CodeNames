import random
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import socket
import os
import threading
import pickle


def get_words_list():
    """
    This function saves all the optional words for the game
    and saves them into a list
    """
    with open("words.txt", "r") as f:
        words_list = f.read()
        words_list = words_list.split()
    return words_list


# --- Classes ----------------------------------------------------------------------
class Player:
    def __init__(self, team, role):
        self.team = team
        self.role = role
        self.ip = ""
        self.teammate = None
        self.socket = None

    def __str__(self):
        st = "team: " + self.team + ", role: " + self.role + ", ip: " + self.ip
        return st

    def send_clue(self, clue):
        msg = 'CLUE' + '~' + clue
        self.teammate.socket.send(msg.encode())
        return msg


def set_teammates(player1: Player, player2: Player):
    player1.teammate = player2
    player2.teammate = [player1]


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
        self.team = ""
        self.role = ""
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
        self.import_random_words()
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


all_to_die = False  # global
players = [Player("blue", "leader"), Player("red", "leader"), Player("blue", "guesser"), Player("red", "guesser")]
for p in players:
    print(p)
set_teammates(players[0], players[2])  # blues
set_teammates(players[1], players[3])  # reds

IP = '0.0.0.0'
port = 1423
board = Board()
board.set_board()


def recv_guess(player: Player):
    try:
        msg = player.socket.recv(1024).decode()
        parts = msg.split('~')
        if parts[0] == "GUES":
            guess = parts[1]
            return guess
        else:
            return "ERRR~200~wrong type of message"
    except:
        return "ERRR~100" # means there was an error in reciving the msg


def send_all(data):
    for pl in players:
        pl.socket.send(data.encode())


def check_guess(guess):
    pass


def send_team(sock, tid):
    to_send = 'TEAM' + '~' + players[tid].team
    sock.send(to_send.encode())
    data = sock.recv(1024).decode()
    return data


def send_role(sock, tid):
    to_send = 'ROLE' + '~' + players[tid].role
    sock.send(to_send.encode())
    data = sock.recv(1024).decode()
    return data


def send_grid(sock):
    global board
    data = pickle.dumps(board)
    to_send = ("GRID" + '~').encode() + pickle.dumps(board.board)
    sock.send(to_send)
    data = sock.recv(1024).decode()
    return data


def protocol_build_reply(request):
    """
    Application Business Logic
    function despatcher ! for each code will get to some function that handle specific request
    Handle client request and prepare the reply info
    string:return: reply
    """
    reply = ""
    request_code = request.decode().split('~')[0]
    request = request.decode()
    if request_code == 'CLUE':
        reply = 'CLUE' + '~' + request.decode().split('~')[1]
    elif request_code[0] == 'EXIT':
        reply = 'EXIT'
    else:
        reply = 'ERRR~002~code not supported' +" - "+ request_code[:5]
        fields = ''
    return reply.encode()


def handle_request(request):
    """
    Handle client request
    tuple :return: return message to send to client and bool if to close the client socket
    """
    try:
        request_code = request[:5]
        to_send = protocol_build_reply(request)
        if request_code == b'EXIT':
            return to_send, True
    except Exception as err:
        print("traceback.format_exc()")  # !!!
        to_send = b'ERRR~001~General error'
    return to_send, False


def handle_client(sock, tid, addr):
    players[tid].socket = sock
    data = sock.recv(1024).decode()
    to_send = ""
    if data[:4] == "HALO":
        data = send_team(sock, tid)
        if data[:4] == "HALO":
            data = send_role(sock, tid)
            if data[:4] == "HALO":
                data = send_grid(sock)
    else:
        print(f'Client {tid} Exit')
        sock.close()



def main():
    global all_to_die
    global players
    global port
    """
    main server loop
    1. accept tcp connection
    2. create thread for each connected new client
    3. wait for all threads
    4. every X clients limit will exit
    """
    threads = []
    srv_sock = socket.socket()
    srv_sock.bind(('0.0.0.0', port))
    srv_sock.listen(4)

    # next line release the port
    srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    i = 0
    while True:
        print('\nMain thread: before accepting ...')
        cli_sock, addr = srv_sock.accept()
        t = threading.Thread(target=handle_client, args=(cli_sock, i, addr))
        t.start()
        i += 1
        threads.append(t)
        if i > 100000000:  # for tests change it to 4
            print('\nMain thread: going down for maintenance')
            break

    all_to_die = True
    print('Main thread: waiting to all clients to die')
    for t in threads:
        t.join()
    srv_sock.close()
    print('Bye ..')


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
