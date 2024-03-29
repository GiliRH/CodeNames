import tkinter as tk

window = tk.Tk()

def open_command():
    open_btn.config(bg='green', fg = 'white')
    close_btn.config(bg='white', fg = 'red')

def close_command():
    open_btn.config(bg='white', fg = 'green')
    close_btn.config(bg='red', fg = 'white')

font=('Old English Text MT', 12)
open_btn = tk.Button(window, text='Open', font=font, fg='green', bg='white', width=5, command=open_command)
open_btn.pack()
close_btn = tk.Button(window, text='Close', font=font, fg='red', bg='white', width=5, command=close_command)
close_btn.pack()

window.mainloop()