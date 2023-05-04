import random
from sympy import *
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import socket
import os
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad

# --- FUNCTIONS --------------------------------------------------------------------

#  diffie-Hellman
def key_exchange(g, p, client):
    # Server generates a private key
    server_private_key = random.randint(1, p - 1)

    # Server computes the public key and sends it to the client
    server_public_key = pow(g, server_private_key, p)

    # Send the public key to the client
    client.send(str(server_public_key).encode())

    # Receive the client's public key
    client_public_key = int(client.recv(1024).decode())

    # Server computes the shared secret key
    server_shared_secret = pow(client_public_key, server_private_key, p)

    # The shared secret key should now be the same as the client's
    print("Shared secret key:", server_shared_secret)
    return server_shared_secret

######################################################################################
# Shared parameters
p = 23
g = 5

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '0.0.0.0'
port = 12345
s.bind((ip, port))

# Wait for client connection
s.listen(1)
print("Waiting for client connection...")
client, addr = s.accept()
print("Client connected:", addr)
######################################################################################

key = key_exchange(g, p, client)

msg = client.recv(1024).decode()
# cipher = AES.new(key, AES.MODE_ECB)
# msg = unpad(cipher.dencrypt(msg),AES.block_size)
print(msg)
showinfo(
        title='Information Recieved',
        message=msg
    )


# Close the connection
client.close()
