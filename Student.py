import xmlrpc.client
import tkinter

def on_closing():
    top.destroy()

def exit():
    byebye = "Student process disconnected"
    proxy.exit(byebye)
    top.destroy()


def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    proxy.student(msg)
    message = "Student: %s     |      Course: %s" %(msg.split(",")[0],msg.split(",")[1])
    msg_list.insert(tkinter.END, message)  

top = tkinter.Tk()
top.title("Student")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar() 
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, width=80, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
exit_button = tkinter.Button(top, text="Exit", command=exit)
exit_button.pack()
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
top.protocol("WM_DELETE_WINDOW", on_closing)
introduction = "I am the student process"
proxy.introduce(introduction)
tkinter.mainloop() 
