import xmlrpc.client
import tkinter
import time
import random
from tkinter import messagebox
from threading import Thread


def on_closing():
    top.destroy()

def exit():
    byebye = "Advisor process disconnected"
    proxy.exit(byebye)
    top.destroy()


def receive():
    introduction = "I am the advisor process"
    proxy.introduce(introduction)
    while True:
        try:
            requests = proxy.advisor()
            print(requests)
            if requests:
                for student, courses in requests.items():
                    for course in courses:
                        if random.randint(1,3) == 1:
                            decision = "approved"
                            proxy.approve(student,course,decision)
                            message = "Student: %s   |    Course: %s     |    decision: approved" %(student,course)  
                            msg_list.insert(tkinter.END, message)             
                        else:
                            decision = "disapproved"
                            proxy.disapprove(student,course,decision)
                            message = "Student: %s   |    Course: %s     |    decision: disapproved" %(student,course)   
                            msg_list.insert(tkinter.END, message)       
            else:
                message = "No message found" 
                msg_list.insert(tkinter.END, message)
                time.sleep(3)
            
        except OSError: 
            break

top = tkinter.Tk()
top.title("Advisor")

messages_frame = tkinter.Frame(top)
# my_msg = tkinter.StringVar() 
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, width=80, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

exit_button = tkinter.Button(top, text="Exit", command=exit)
exit_button.pack()

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
receive_thread = Thread(target=receive)
receive_thread.start()
top.protocol("WM_DELETE_WINDOW", on_closing)
tkinter.mainloop()
