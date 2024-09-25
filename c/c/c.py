
import socket
import threading
import random
from tkinter import *

#�Pserver�إ߳s�u
SERVER = "192.168.1.105"
PORT = 5055
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(ADDRESS)
        

room=input("chosing chatroom:dirty/clean:")
client.send(room.encode(FORMAT))
age=input("input your age:")
client.send(age.encode(FORMAT))
    


class GUI:
    def __init__(self):      

        self.Window = Tk()
        name = 'user-'+str(random.randint(1,100)) #name�Ʀr�H���M�w
        self.layout(name)
        
        #�إ߷sthread�B�z������ơA�~���|�d��
        rcv = threading.Thread(target=self.receive)
        rcv.start()

        self.Window.mainloop()        


    def layout(self, name):
        self.name = name

        self.Window.title("CHATROOM")
        self.Window.resizable(width=True,
                              height=True)
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
        
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name, 
                               font="Helvetica 13 bold",
                               pady=5)  #����W�U���Ŷ�
        self.labelHead.place(relwidth=1)
        
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9") 
        self.line.place(relwidth=1, #�۹�D�������e��
                        rely=0.07, #�۹�D������y�y��
                        relheight=0.012) #�۹�D�������e��
 
        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5, #���󥪥k���Ŷ�
                             pady=5) 
        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)
 
        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80) 
        self.labelBottom.place(relwidth=1,
                               rely=0.825)
 
        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)  #�۹�D������x�y��
        self.entryMsg.focus()
 

        self.buttonMsg = Button(self.labelBottom,
                            text="Send",
                            font="Helvetica 10 bold",
                            width=20,
                            bg="#ABB2B9",
                            #�N��J�Ϫ���r�A���sendButton()�B�z
                            command=lambda: self.sendButton(self.entryMsg.get())) 
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)
 
        self.textCons.config(cursor="arrow")
 
        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1,
                        relx=0.974) 
        scrollbar.config(command=self.textCons.yview)
 
        self.textCons.config(state=DISABLED)#��ܰϤ��\�ܧ�
 
    #�إ߷sthread�B�z�����T��
    def receive(self):



        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
 
                #�즸�s�u�Aserver�|�e��'NAME'�Aclient�|�^�Ǧۤv��name
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else: 
                    #����Aserver�e�Ӫ��T���A���|�L�ܹ�ܰ�
                    self.textCons.config(state=NORMAL) #��ܰϳ\�i�[�J
                    self.textCons.insert(END,message+"\n\n") #END����ܰϪ���J�I
                    self.textCons.config(state=DISABLED)#��ܰϤ��\�ܧ�
                    self.textCons.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!")
                client.close()
                break
    #���Usend����
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)#��ܰϤ��\�ܧ�
        self.msg = msg
        self.entryMsg.delete(0, END)#�N��J�ϲM��
        message = (f"{self.name}: {self.msg}")
        client.send(message.encode(FORMAT))      

g = GUI()