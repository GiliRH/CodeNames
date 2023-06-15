from random import randint
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox
import socket
import os
import random
import pickle
import threading
import queue
import time


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
        st += '\nteam:' + self.team
        st += '\nrole:' + self.role
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


port = 2134
root = tk.Tk()
ip = '127.0.0.1'
sock = socket.socket()
clue = ""
connected = False
board = Board()
grid_buttons = []
btn = None
the_queue = queue.Queue()


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


def create_root_leader(team, role):
    global root
    global btn
    global grid_buttons
    root.title('team: ' + team + 'role: ' + role)
    root.config(bg='dark slate gray')

    l = tk.Label(root, text="Enter Clue:")
    l.grid(row=0, column=0, columnspan=1)

    l.config(font=("Courier", 12))
    enter_clue = tk.Entry(root, width=22)
    enter_clue.grid(row=0, column=1, columnspan=3)
    enter_clue.config(font=("Courier", 14))

    btn = tk.Button(root, height=1, width=12, text="Enter", state=tk.DISABLED, command=send_clue)
    btn.grid(row=0, column=4, columnspan=1)
    for r in range(0, 5):
        for c in range(0, 5):
            b = tk.Button(root, text=board.board[5 * r + c].word, bg=board.board[5 * r + c].type, borderwidth=1,
                          height=5, width=10, state=tk.DISABLED)
            b.grid(row=r + 1, column=c, padx=2, pady=2)
            grid_buttons.append(b)



def create_root_guesser(team, role):
    global root
    global grid_buttons
    root.title('team: ' + team + ' role: ' + role)
    root.config(bg='dark slate gray')

    l = tk.Label(root, text='Clue: ' + clue)
    l.grid(row=0, column=0, columnspan=5)
    l.config(font=("Courier", 14))

    for r in range(0, 5):
        for c in range(0, 5):
            b = tk.Button(root, text=board.board[5 * r + c].word, bg='snow', borderwidth=1, height=5, width=10,
                          command=lambda r=r, c=c: reveal_card(r, c))
            b.grid(row=r + 1, column=c, padx=2, pady=2)
            grid_buttons.append(b)



def reveal_card(row, col):
    global sock
    global root
    global board
    global grid_buttons
    guess = board.board[5 * row + col].word
    print("row:", row, "col:", col, "--> text: ", guess)
    grid_buttons[5 * row + col].config(bg=board.board[5 * row + col].type)


def color_greed(grid):
    global root
    for r in range(0, 5):
        for c in range(0, 5):
            tk.Button(root, borderwidth=1).grid(row=r, column=c).config(bg=board.board[5 * r + c].type)
    root.mainloop()


def send_guess(row, col, board):
    pass


def send_clue(enter_clue):
    global clue
    global sock
    clue = enter_clue.get()
    print("clue: ", clue)
    msg = "CLUE" + '~' + clue
    sock.send(msg.encode())


def make_turn_leader():
    pass


def make_turn_guesser(clue):
    pass


def make_turn():
    pass


def able_entry(button):
    button.config(state=tk.NORMAL)


def disable_entry(button):
    button.config(state=tk.DISABLED)


def accept_team(reply):
    global board
    global sock
    fields = []
    if '~' in reply:
        fields = reply.split('~')
    t = fields[1]
    board.team = t
    print(board)
    sock.send("HALO".encode())


def accept_role(reply):
    global board
    global sock
    fields = []
    if '~' in reply:
        fields = reply.split('~')
    r = fields[1]
    print(r)
    board.role = r
    print(board)
    sock.send("HALO".encode())


def accept_grid(reply):
    global board
    global sock
    global root
    code = reply[:4].decode()
    board.board = pickle.loads(reply[5:])
    print(board)

    sock.send("HALO".encode())



def end_process():
    global sock
    global root

    showinfo(title="END", message="THE GAME HAS ENDED")
    sock.close()
    root.destroy()


def on_closing():
    global sock
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        print("Sending --> EXIT")
        sock.send("EXIT".encode())
        # end_process()


def protocol_parse_reply(reply):
    """
    parse the server reply and prepare it to user
    return: answer from server string
    """

    to_show = 'Invalid reply from server'
    try:
        if reply[:4].decode() == "GRID":
            to_show = "GRID" + " "
        else:
            reply = reply.decode()
            if '~' in reply:
                fields = reply.split('~')
            code = reply[:4]
            if code == 'TEAM':
                to_show = 'TEAM ' + fields[1]
            elif code == 'ROLE':
                to_show = 'ROLE ' + fields[1]
            elif code == 'TURN':
                to_show = 'TURN'
            elif code == 'ERRR':
                to_show = 'Server return an error: ' + fields[1] + ' ' + fields[2]
            elif code == 'EXIT':
                to_show = 'Server acknowledged the exit message'
    except Exception as err:
        print('3Server replay bad format : ', err)
    return to_show


def handle_reply(reply):
    to_show = protocol_parse_reply(reply)
    if to_show != '':
        print('\n==========================================================')
        print(f'  SERVER Reply: {to_show}   |')
        print('==========================================================')
    try:
        if reply[:4].decode() == "GRID":
            accept_grid(reply)
            print("done")
        else:
            reply = reply.decode()
            print("reply:", reply)
            if '~' in reply:
                fields = reply.split('~')
            code = reply[:4]
            if code == 'TEAM':
                accept_team(reply)
            elif code == 'ROLE':
                accept_role(reply)
            elif code == 'REVL':
                pass
            elif code == 'TURN':  # !! finish
                make_turn()
            elif code == 'TWIN':
                pass
            elif code == 'LOSE':
                pass
            elif code == 'EXIT':
                print("Exiting")
                end_process()
    except Exception as err:
        print('1Server replay bad format : ', err)


def start_root():
    global root
    global board
    if board.role == "leader":
        create_root_leader(board.team, board.role)
    if board.role == "guesser":
        create_root_guesser(board.team, board.role)
    root.mainloop()


def callback_root():
    global root
    global ip
    global port
    # global clue
    global sock
    global connected
    global root
    global board

    try:
        message = the_queue.get(block=False)
    except queue.Empty:
        # let's try again later
        root.after(100, callback_root)
        return

    print('callback_root got', message[:4].decode())
    if connected:
        # we're not done yet, let's do something with the message and
        # come back later
        print("MSG -->", message[:4].decode())
        print("callback")
        handle_reply(message)
        root.after(100, callback_root)


def thread_target():
    global ip
    global port
    # global clue
    global sock
    global connected
    global root
    global board

    # to_send = "HALO"
    while connected:
        try:
            print("hello th(e)re-ad-")

            # print("to send...", to_send)
            # sock.send(to_send.encode())
            print("receving...")
            byte_data = sock.recv(1024)
            if byte_data == b'':
                print('Seems server disconnected abnormal')
                break
            print("recived -->", byte_data[:4].decode())
            the_queue.put(byte_data)

            if not connected:
                print('Will exit ...')
                connected = False
                break
        except socket.error as err:
            print(f'Got socket error: {err}')
            break
        except Exception as err:
            print(f'General error: {err}')
            print(traceback.format_exc())
            break

    # let's tell after_callback that this completed
    print('thread_target puts None to the queue')
    the_queue.put(None)


def begin():
    to_send = "HALO"
    try:
        for i in range (3):
            sock.send(to_send.encode())
            byte_data = sock.recv(1024)
            print(byte_data[:4].decode())
            if byte_data == b'':
                print('Seems server disconnected abnormal')
                break
            handle_reply(byte_data)
    except Exception as err:
        print('2Server replay bad format : ', err)


def main():
    global ip
    global port
    # global clue
    global sock
    global connected
    global root
    global board

    threads = []
    user_ip = input("Enter ip (nothing entered --> 127.0.0.1)")
    if user_ip != "":
        ip = user_ip
    sock = socket.socket()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    try:
        sock.connect((ip, port))
        print(f'Connect succeeded {ip}:{port}')
        connected = True
        begin()
        print("openning thread...")
        threading.Thread(target=thread_target).start()
        print("starting callback...")
        root.after(2000, callback_root)
        start_root()
        # connected = True
        # to_send = "HALO"
        # while connected:
        #     try:
        #         print("hello")
        #
        #         print("to send...", to_send)
        #         sock.send(to_send.encode())
        #         print("receving...")
        #         byte_data = sock.recv(1024)
        #         print(byte_data[:4].decode())
        #         if byte_data == b'':
        #             print('Seems server disconnected abnormal')
        #             break
        #         handle_reply(byte_data)
        #
        #         if not connected:
        #             print('Will exit ...')
        #             connected = False
        #             break
        #     except socket.error as err:
        #         print(f'Got socket error: {err}')
        #         break
        #     except Exception as err:
        #         print(f'General error: {err}')
        #         print(traceback.format_exc())
        #         break


    except:
        print(f'Error while trying to connect.  Check ip or port -- {ip}:{port}')

    print('Bye')
    try:
        sock.close()
    except:
        print("already closed")


if __name__ == '__main__':
    main()