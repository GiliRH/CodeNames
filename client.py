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


#  diffie-Hellman
def exchange_key(p,g,s):
    # Receive the server's public key
    server_public_key = int(s.recv(1024).decode())

    # Client generates a private key
    client_private_key = random.randint(1, p - 1)

    # Client computes the public key and sends it to the server
    client_public_key = pow(g, client_private_key, p)
    s.send(str(client_public_key).encode())

    # Client computes the shared secret key
    client_shared_secret = pow(server_public_key, client_private_key, p)

    # The shared secret key should now be the same as the server's
    print("Shared secret key:", client_shared_secret)
    return client_shared_secret

######################################################################################
# Shared parameters
p = 23
g = 5

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '127.0.0.1'
port = 12345
s.connect((ip, port))
######################################################################################

key = exchange_key(p, g, s)

# # root window
# root = tk.Tk()
# root.geometry("300x150")
# root.resizable(False, False)
# root.title('Sign In')
#
# # store email address and password
# email = tk.StringVar()
# password = tk.StringVar()
#
# # Sign in frame
# signin = ttk.Frame(root)
# signin.pack(padx=10, pady=10, fill='x', expand=True)
#
# # email
# email_label = ttk.Label(signin, text="Email Address:")
# email_label.pack(fill='x', expand=True)
#
# email_entry = ttk.Entry(signin, textvariable=email)
# email_entry.pack(fill='x', expand=True)
# email_entry.focus()
#
# # password
# password_label = ttk.Label(signin, text="Password:")
# password_label.pack(fill='x', expand=True)
#
# password_entry = ttk.Entry(signin, textvariable=password, show="*")
# password_entry.pack(fill='x', expand=True)
#
# # login button
# login_button = ttk.Button(signin, text="Login", command=login_clicked)
# login_button.pack(fill='x', expand=True, pady=10)
#
# root.mainloop()

# Close the connection
s.close()
