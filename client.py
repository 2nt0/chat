from tkinter import *
from tkinter.ttk import *
from socket import *
from _thread import *
from time import sleep
try:
    from chatsave import *
except:
    open('chatsave.py', 'w').write('addr=\'localhost\'\nport=2428')
    from chatsave import *

srv=socket(AF_INET,SOCK_STREAM)
conn=True
try:    srv.connect((addr,port))
except:    conn=False

def write_to(out,msg):
    out.configure(state=NORMAL)
    out.insert(END,str(msg)+'\n')
    out.configure(state=DISABLED)
    out.see(END)

def srv_thread(addr,out,conn):
    global srv
    global conn_lbl
    if not(conn):
        never=True
    else:
        never=False
    
    while conn:
        try:
            msg=srv.recv(65536).decode()
            write_to(out,msg)
        except:
            conn=False
            srv.shutdown(SHUT_RDWR)
            srv.close()
            srv=socket(AF_INET,SOCK_STREAM)
    
    if never:    write_to(out,' --- Server '+addr+' not online ---')
    else:    write_to(out,' --- Server diconnected ---')
    conn_lbl.configure(text='Not connected')
    
    while not(conn):
        try:
            srv.connect((addr,port))
            conn=True
            write_to(out,'\n --- Server connected ---')
            conn_lbl.configure(text='Connected to')
            srv_thread(addr,out,conn)
        except:
            pass

def submit(e):
    msg=e.widget.get('1.0',END)
    e.widget.delete('1.0',END)
    msg=msg.replace('\n','')
    
    if len(msg) > 1:
        try:
            srv.send(msg.encode())
            write_to(main_out,'<You> '+msg)
        except:
            pass

def save(e):
    addr=addr_txt.get('1.0',END)[:-1]
    port=int(port_txt.get('1.0',END)[:-1])
    open('chatsave.py', 'w').write('addr=\''+addr+'\'\nport='+str(port))
    sleep(0.5)
    addr_txt.delete('1.0',END)
    port_txt.delete('1.0',END)
    port_txt.insert(END,str(port))
    addr_txt.insert(END,addr)
    

window=Tk()
window.title('Chatroom (v1.0-snapshot)')

tab_mstr=Notebook(window)
chat_tab=Frame(tab_mstr)
tab_mstr.add(chat_tab,text='Chat')
tab_mstr.pack(expand=0,fill='both')

conn_lbl=Label(chat_tab,text='Connected to')
conn_lbl.grid(column=0,row=0,padx=5,pady=5,sticky=W)
addr_frm=Frame(chat_tab)
addr_frm.grid(column=1,row=0,padx=5,pady=5,sticky=E)
port_txt=Text(addr_frm,height=1,width=5)
port_txt.grid(column=2,row=0)
port_txt.insert(END,str(port))
port_txt.bind('<Return>',save)
Label(addr_frm,text=':').grid(column=1,row=0)
addr_txt=Text(addr_frm,height=1,width=15)
addr_txt.grid(column=0,row=0)
addr_txt.insert(END,addr)
addr_txt.bind('<Return>',save)

main_out=Text(chat_tab,height=30,width=50,state=DISABLED)
main_out.grid(column=0,row=1,padx=5,columnspan=2)
main_in=Text(chat_tab,height=1,width=50)
main_in.grid(column=0,row=2,padx=5,pady=5,columnspan=2)
main_in.bind('<Return>',submit)

start_new_thread(srv_thread,(addr,main_out,conn))
window.mainloop()