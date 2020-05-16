import tkinter
from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread

def on_closing():
    top.destroy()

def student(msg):
    name = msg.split(",")[0]
    course = msg.split(",")[1]
    if name not in requests:
        temp = []
        temp.append(course)
        requests[name] = temp
    else:
        requests[name].append(course)
   

def advisor():
    if(requests):
        return requests
    else:
        return None

def notify():
    if(decisions):
        return decisions
    else:
        return None

def approve(student, course, decision):
    temp = []
    temp.append(student)
    temp.append(course)
    temp.append(decision)
    decisions.append(temp)
    requests[student].remove(course)
    if len(requests[student]) == 0:
        del requests[student]
    return

def disapprove(student, course, decision):
    temp = []
    temp.append(student)
    temp.append(course)
    temp.append(decision)
    decisions.append(temp)
    requests[student].remove(course)
    if len(requests[student]) == 0:
        del requests[student]
    return

def removeDecision(item):
    decisions.remove(item)
    return

def introduce(introduction):
    msg_list.insert(tkinter.END, introduction)
    return

def exit(byebye):
    msg_list.insert(tkinter.END, byebye)
    return


def start():
    server = SimpleXMLRPCServer(("localhost", 8000),allow_none=True)
    server.register_function(student)
    server.register_function(advisor)
    server.register_function(notify)
    server.register_function(approve)
    server.register_function(disapprove)
    server.register_function(removeDecision)
    server.register_function(introduce)
    server.register_function(exit)
    server.serve_forever()
    


requests = {}
decisions = []
top = tkinter.Tk()
top.title("Server")

messages_frame = tkinter.Frame(top)
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, width=80, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

exit_button = tkinter.Button(top, text="Exit", command=on_closing)
exit_button.pack()

receive_thread = Thread(target=start)
receive_thread.start()
top.protocol("WM_DELETE_WINDOW", on_closing)
tkinter.mainloop() 