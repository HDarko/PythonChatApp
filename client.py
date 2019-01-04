#!/usr/bin/env python3

"""Script for Tkinter gui client."""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter



def receive():
    """Handles receiving of messages."""

    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError : #Possibly client has left the chat.
            break


def send(event=None): #event is passed by binders
    """Handles sending of messages."""
    msg = my_msg.get() #gets user input
    my_msg.set("") #Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This functions is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

#----------------------------------------Tkinter-----------------------------------------
top = tkinter.Tk()
top.title("Stryfe")
top.configure(background='#E8E8E8')
top.iconbitmap('logo.ico')

#----------------------Sidebars----------------------------------
#logo = tkinter.PhotoImage(file="logo(1).gif")
#imagebar = tkinter.Label(top, width="10", height="10", relief=tkinter.FLAT, bg='#303030', image=logo)
#imagebar.pack(expand=True, fill='both', side='left', anchor='nw')

sidebar = tkinter.Label(top, width="20", height="20", relief=tkinter.FLAT, bg='#303030', text="User Guide" +'\n'+'\n'+"To whisper use:"+'\n'+ "/[username of the"+'\n'+" person you want"+'\n'+" to whisper]" + '\n'+'\n'+"Display the current"+'\n'+ "users in chat: "+'\n'+"Type @", fg="white", font=('Helvetica',8,'bold'))
sidebar.pack(expand=True, fill='both', side='left', anchor='n')


sidebar2=tkinter.Frame(top, width="60", height="20", relief=tkinter.FLAT, bg='#505050')
sidebar2.pack(expand=True, fill='both', side='left', anchor='nw')

#sidebar3=tkinter.Frame(top, width="10", height="5", relief=tkinter.FLAT, bg='#808080')
#sidebar3.pack(expand=True, fill='both', side='bottom', anchor='sw')



messages_frame = tkinter.Frame(top)

my_msg = tkinter.StringVar() # For the messages to be sent.
my_msg.set("Type a message...")


scrollbar = tkinter.Scrollbar(messages_frame) # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=20, width=110, yscrollcommand=scrollbar.set, bg='white', relief=tkinter.FLAT)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()
#------------------HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE-----------------------------------------
loadimage = tkinter.PhotoImage(file="send.png")
#------------------HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE-----------------------------------------
entry_field = tkinter.Entry(top, textvariable=my_msg, relief=tkinter.FLAT, width=90, bg="#E8E8E8")
entry_field.bind("<Return>", send)
entry_field.pack(side="left", pady="20", anchor="s")
entry_field.config(font=("Helvetica", 10))
#------------------HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE-----------------------------------------
send_button = tkinter.Button(top, text="Send", command=send, image=loadimage, height="24", width="24", bg="#E8E8E8")

send_button["border"] = "0"
send_button.pack(side="left", padx="10")



top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----

HOST="159.28.40.163"
PORT=65432
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
