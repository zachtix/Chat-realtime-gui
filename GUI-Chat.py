from tkinter import *
from tkinter import ttk, simpledialog, messagebox
import tkinter.scrolledtext as st
import random
import json

######################################
import socket
import threading
import sys

PORT = 7500
BUFSIZE = 4096
SERVERIP = '127.0.0.1'

def serverHandler(client):
  while True:
    try:
      data = client.recv(BUFSIZE)
    except:
      print('ERROR')
      break
    if (not data) or (data.decode('utf-8') == 'q'):
      print('OUT!')
      break

    # print('USER : ', data.decode('utf-8'))
    allmsg.set(data.decode('utf-8'))
    chatbox.insert(INSERT, allmsg.get())
    chatbox.yview(END)
  
  client.close()
  messagebox.showerror('Disconnect', 'Disconnect')
######################################


GUI = Tk()
GUI.geometry('650x750+300+50')
GUI.title('Chat Realtime')

FONT1= ('Angsana New', 35)
FONT2= ('Angsana New', 20)

F1 = Frame(GUI)
F1.place(x=5, y=5)

allmsg = StringVar()

chatbox = st.ScrolledText(F1, width=39, heigh=10, font=FONT1)
chatbox.pack(expand=True, fill='x')

v_msg = StringVar()

F2 = Frame(GUI)
F2.place(x=20, y=650)

E1 = ttk.Entry(F2, textvariable=v_msg, width=50, font=FONT2)
E1.pack(ipady=20)


def SendMessage(event=None):
    msg = v_msg.get()
    allmsg.set(msg)
    client.sendall(msg.encode('utf-8'))
    # chatbox.insert(INSERT, allmsg.get())
    # chatbox.yview(END)
    v_msg.set('') #clear msg
    E1.focus()



F3 = Frame(GUI)
F3.place(x=500, y=650)
B1 = ttk.Button(F3, text='Send', command=SendMessage)
B1.pack(ipadx=25, ipady=30)

E1.bind('<Return>', SendMessage)

username = StringVar()

getname = simpledialog.askstring('name', 'What is your name?')
if getname == None:
  num = random.randint(10000,99999)
  getname = str(num)
username.set(getname)
chatbox.insert(INSERT, 'Hello ' + getname + '\n')


global client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
  client.connect((SERVERIP, PORT))
  firsttext = 'NAME|' + username.get()
  client.send(firsttext.encode('utf-8'))
  task = threading.Thread(target = serverHandler, args = (client,))
  task.start()
except:
  print('ERROR')
  messagebox.showerror('Connection Fail', 'Connection Fail')

GUI.mainloop()