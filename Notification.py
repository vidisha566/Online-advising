import xmlrpc.client
import tkinter
import time
import random
from threading import Thread

def on_closing():
    top.destroy()

def exit():
    byebye = "Notification process disconnected"
    proxy.exit(byebye)
    top.destroy()


def receive():
    introduction = "I am the notification process"
    proxy.introduce(introduction)
    while True:
        try:
            decisions = proxy.notify()
            print(decisions)
            if decisions:
                for item in decisions:
                    proxy.removeDecision(item)
                    student = item[0]
                    course = item[1]
                    decision = item[2]
                    message = "Student: %s   |    Course: %s     |    decision: %s" %(student,course,decision)  
                    msg_list.insert(tkinter.END, message)
            else:
                message = "No message found" 
                msg_list.insert(tkinter.END, message)
                time.sleep(7)
            
        except OSError: 
            break


decisions = {}
top = tkinter.Tk()
top.title("Notification")

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
