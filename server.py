from socket import *
from _thread import *

srv=socket(AF_INET,SOCK_STREAM)
srv.bind(('0.0.0.0',2428))
srv.listen(5)
clients=[]

def client_thread(conn,addr):
    while True:
        try:
            msg_recv=conn.recv(65536).decode()
            if msg:
                msg_send='<'+addr[0]+'> '+msg_recv
                print(msg_send)
                broadcast(msg_send.encode(),conn)
        except:
            conn.close()
            clients.remove(conn)
            msg=addr[0]+' disconnected'
            print(msg)
            broadcast(msg.encode(),conn)
            exit()

def broadcast(msg,conn):
    for client in clients:
        if client != conn:    client.send(msg)

while True:
    conn,addr=srv.accept()
    clients.append(conn)
    msg=addr[0]+' connected'
    print(msg)
    broadcast(msg.encode(),conn)
    start_new_thread(client_thread,(conn,addr))