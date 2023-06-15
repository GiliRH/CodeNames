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


def quit():
    global root
    root.quit()

root = tk.Tk()
while True:
    tk.Button(root, text="Quit", command=quit).pack()
    root.mainloop()