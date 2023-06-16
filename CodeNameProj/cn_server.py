# import tkinter as tk
#
# window = tk.Tk()
#
# def open_command():
#     open_btn.config(bg='green', fg = 'white')
#     close_btn.config(bg='white', fg = 'red')
#
# def close_command():
#     open_btn.config(bg='white', fg = 'green')
#     close_btn.config(bg='red', fg = 'white')
#
# font=('Old English Text MT', 12)
# open_btn = tk.Button(window, text='Open', font=font, fg='green', bg='white', width=5, command=open_command)
# open_btn.pack()
# close_btn = tk.Button(window, text='Close', font=font, fg='red', bg='white', width=5, command=close_command)
# close_btn.pack()
#
# window.mainloop()
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

    def send_clue(self, clue, tid):
        global turn
        print("clue --> ", clue)
        msg = 'CLUE' + '~' + clue
        turn += 1
        sockets[turn].send(msg.encode())
        print(msg)
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
        self.blue = 8
        self.red = 8
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
players = [Player("blue", "leader"), Player("blue", "guesser"), Player("red", "leader"), Player("red", "guesser")]
for p in players:
    print(p)
sockets = []
set_teammates(players[0], players[2])  # blues
set_teammates(players[1], players[3])  # reds
turn = 0

IP = '0.0.0.0'
port = 1234
board = Board()
board.set_board()


def recv_guess(player: Player, msg):
    try:
        parts = msg.split('~')
        if parts[0] == "REVL":
            row = parts[1]
            col = parts[2]
            color = board.board[int(row) * 5 + int(col)].type
            print("COLOR", color)
            spy = ""
            if color == "sky blue":
                board.blue -= 1
                print("BLUE", str(board.blue))
            if color == "firebrick2":
                board.red -= 1
                print("RED", str(board.red))
            if color == "AntiqueWhite2":
                print("villager")
            if color == "purple":
                spy = player.team
            return row, col ,spy
        else:
            return "ERRR~200~wrong type of message"
    except Exception as err:
        print("ERROR -->", err)
        return "ERRR~100" # means there was an error in reciving the msg


def send_all(data):
    i = 0
    for pl in sockets:
        if pl is not None:
            i += 1
            pl.send(data.encode())
            print("sent", i, data)


def end_game(spy):
    global all_to_die
    global board
    i = 0
    if board.blue == 0 or spy == "red":
        print("BLUE WIN")
        for pl in sockets:
            if players[i].team == "blue":
                pl.send("TWIN".encode())
            if players[i].team == "red":
                pl.send("LOSE".encode())
            i+=1
        end_all()
        all_to_die = True
    elif board.red == 0 or spy == "blue":
        print("RED WIN")
        for pl in sockets:
            if players[i].team == "red":
                pl.send("TWIN".encode())
            if players[i].team == "blue":
                pl.send("LOSE".encode())
        i += 1
        end_all()
        all_to_die = True


def send_team(sock, tid):
    to_send = 'TEAM' + '~' + players[tid].team
    sock.send(to_send.encode())
    data = sock.recv(1024).decode()
    return data


def send_all_card(row, col, tid):
    to_send = 'REVL' + '~' + row + '~' + col
    row, col, spy = recv_guess(players[tid], to_send)
    send_all(to_send)
    end_game(spy)
    return to_send


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


def end_all():
    print("end_all")
    send_all("EXIT")
    return "End all processes"


def next_turn(tid):
    global turn
    if turn % 4 == tid:
        print("turn", turn % 4)
        sockets[tid].send("TURN".encode())


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
        reply = 'ERRR~002~code not supported' + " - " + request_code[:5]
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
    global turn
    finish = False
    print(f'New Client number {tid} from {addr}')
    players[tid].socket = sock
    sockets.append(sock)
    data = sock.recv(1024).decode()
    print(f"client {tid}: {data}")
    to_send = ""
    if data[:4] == "HALO":
        print("sending team")
        send_team(sock, tid)
        data = sock.recv(1024).decode()
        print(f"client {tid}: {data}")
        if data[:4] == "HALO":
            print("sending role")
            send_role(sock, tid)
            data = sock.recv(1024).decode()
            print(f"client {tid}: {data}")
            if data[:4] == "HALO":
                print("sending grid")
                send_grid(sock)

    while not finish:
        if all_to_die:
            print('will close due to main server issue')
            break
        try:
            next_turn(tid)
            data = sock.recv(1024).decode()
            fields = []
            if '~' in data:
                fields = data.split('~')
            print("data -->", data)
            print(f"client {tid}: {data}")
            to_send = ""
            if data[:4] == "HALO":
                print("done")
            elif data[:4] == "GUES":
                data = send_all_card(fields[1], fields[2], tid)
            elif data[:4] == "CLUE":
                players[tid].send_clue(fields[1], tid)
            elif data[:4] == "ENDT":
                turn+=1
                next_turn(turn % 4)
            elif data[:4] == "EXIT":
                data = end_all()
            else:
                print(f'Client {tid} Exit')
                sock.close()
        except socket.error as err:
            print(f'Socket Error exit client loop: err:  {err}')
            break
        except Exception as err:
            print(f'General Error %s exit client loop: {err}', addr)
            # print(traceback.format_exc())
            # print(traceback.format_exc())
            break


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
