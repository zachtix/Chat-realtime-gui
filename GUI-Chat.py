from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as st

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
    allmsg.set(msg + '\n')
    chatbox.insert(INSERT, allmsg.get())
    chatbox.yview(END)
    v_msg.set('') #clear msg
    E1.focus()



F3 = Frame(GUI)
F3.place(x=500, y=650)
B1 = ttk.Button(F3, text='Send', command=SendMessage)
B1.pack(ipadx=25, ipady=30)

E1.bind('<Return>', SendMessage)

GUI.mainloop()