import base_net
from tkinter import *
import os
import sys
import json


class ClientUi(base_net.Client):
    def __init__(self, *args):
        super().__init__(*args)

    def on_receive_data(self, data):
        _json = json.loads(data)
        label["text"] += _json["message"] + "\n"
    

PORT = 50000
ADDRESS = "localhost"

def on_click():
    if ent.get() == "": return

    client.send_data(ent.get())
    ent.delete(0, END)   

def on_closing():
    client.disconnect()
    root.destroy()
    sys.exit()

client = ClientUi(ADDRESS, PORT)
client.start()

root = Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.geometry("400x400")
root.title("Chat")

label = Label(root)
label.pack(side=TOP, fill=X)

bottom_frame = Frame(root)
bottom_frame.pack(side=BOTTOM)

ent = Entry(bottom_frame, font="Arial, 24")
ent.pack(fill=X)

butt = Button(bottom_frame, text="Send")
butt.config(command=on_click)
butt.pack()

root.mainloop()