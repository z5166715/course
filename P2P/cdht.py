import sys
import os
import time
import threading
from socket import *


filename = sys.argv[0]
arg1 = int(sys.argv[1])
arg2 = int(sys.argv[2])
arg3 = int(sys.argv[3])

print("the number of argument is",len(sys.argv)-1,f'They are {arg1},{arg2},{arg3}')


port = 50000 + arg1
addr = ("127.0.0.1", port)
U_addr =("",port)


def UDP_thread_function(arg1,arg2,arg3,addr):
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(addr)
    while True:
        
        message = b"Ping message"
        des_port1 = 50000 + arg2
        des_port2 = 50000 + arg3
        des_addr1 = ("",des_port1)
        des_addr2 = ("",des_port2)
        s.sendto(message,des_addr1)
        s.sendto(message,des_addr2)

        data, server = s.recvfrom(1024)
        pe_number = server[1]-50000
        if data == b"Ping message":
            respond = b"Respond message"
            s.sendto(respond,server)
            print(f'A ping request message was received from Peer {pe_number}')
        elif data == b"Respond message":
            print(f'A ping  response message was received from Peer {pe_number}')
        time.sleep(3)


def request_file_value(message):
    newlist = filter(str.isdigit,message)
    l = list(newlist)
    new_value =int("".join(l))
    return new_value

def new_c_s(message):
    global arg1
    global arg2
    global addr

    TCP_des_port = 50000+arg2
    TCP_des_addr = ("127.0.0.1",TCP_des_port)
    
    TCP_c_port = 60000+arg1
    TCP_c_addr = ("127.0.0.1",TCP_c_port)

    new_c = socket(AF_INET,SOCK_STREAM)
    new_c.bind(TCP_c_addr)

    new_c.connect(TCP_des_addr)
    new_c.send(message.encode('utf-8'))
    print("File request message has been forwarded to my successor.")

    new_c.close()

def new_c_so(so_port,file):
    global arg1
    global arg2
    global addr

    TCP_des_port = so_port
    TCP_des_addr = ("127.0.0.1",TCP_des_port)
    
    TCP_c_port = 60000+arg1
    TCP_c_addr = ("127.0.0.1",TCP_c_port)

    new_c = socket(AF_INET,SOCK_STREAM)
    new_c.bind(TCP_c_addr)

    new_c.connect(TCP_des_addr)
    tuple_r = ('R',file)
    r_message = str(tuple_r)
    so_peer = so_port - 50000
    new_c.send(r_message.encode('utf-8'))
    print(f"A response message, destined for peer{so_peer}, has been sent.")
       
    new_c.close()

def de_p_f(message):
    global arg1
    global arg2
    global addr

    TCP_des_port = 50000+arg2
    TCP_des_addr = ("127.0.0.1",TCP_des_port)
    
    TCP_c_port = 60000+arg1
    TCP_c_addr = ("127.0.0.1",TCP_c_port)
    new_c = socket(AF_INET,SOCK_STREAM)

    new_c.connect(TCP_des_addr)
    new_c.send(message.encode('utf-8'))

    new_c.close()
    
    
def UDP_thread_job():
    global arg1
    global arg2
    global arg3
    
    N_port = 50000 + arg1
    
    N_addr =("",port)
    
    UDP_thread_function(arg1,arg2,arg3,N_addr)

def thread_job_c():
    global arg1
    global arg2
    global arg3
    global addr
    global U_addr
    


    TCP_des_port = 50000+arg2
    TCP_des_addr = ("127.0.0.1",TCP_des_port)
    
    TCP_c_port = 60000+arg1
    TCP_c_addr = ("127.0.0.1",TCP_c_port)
        
    
    



    while True:
        sentence = input('Which file request or quit:\n')
        if sentence == "quit":
            c_s = socket(AF_INET,SOCK_STREAM)
            c_s.bind(TCP_c_addr)
            c_s.connect(TCP_des_addr)
            fi_se_tuple = ("quit",arg1,arg2,arg3)
            fi_se = str(fi_se_tuple)
            c_s.send(fi_se.encode('utf-8'))
            os._exit(0)
        else:
            c_s = socket(AF_INET,SOCK_STREAM)
            c_s.bind(TCP_c_addr)
            c_s.connect(TCP_des_addr)
            file_value = request_file_value(sentence)
            sentence_value = file_value%256
            tuple_hash = (arg1,sentence_value,file_value)
            str_hash = str(tuple_hash)
            c_s.send(str_hash.encode('utf-8'))
            TCP_respond = c_s.recv(1024)





def thread_job_s():
    global arg1
    global arg2
    global arg3
    global addr


    s_s = socket(AF_INET,SOCK_STREAM)
    s_s.bind(addr)
    s_s.listen(5)
    print("The server is ready to receive")


        

    

    while True:
        connect_s,sou_addr = s_s.accept()
        sou_peer = sou_addr[1]-60000
        sentence = connect_s.recv(1024)
        sentence = sentence.decode('utf-8')
        sentence_tuple = tuple(eval(sentence))
        if sentence_tuple[0] == "quit":
            if arg2 == sentence_tuple[1]:
                de_peer = sentence_tuple[1]
                print(f"Peer {de_peer} will depart from the network.\n")
                arg2 = sentence_tuple[2]
                print(f"My first successor is now peer {arg2}.\n")
                arg3 = sentence_tuple[3]
                print(f"My second successor is now peer {arg3}.\n")
            elif arg3 == sentence_tuple[1]:
                de_peer = sentence_tuple[1]
                print(f"Peer {de_peer} will depart from the network.\n")
                print(f"My first successor is now peer {arg2}.\n")
                arg3 = sentence_tuple[2]
                print(f"My second successor is now peer {arg3}.\n")
                de_p_f(sentence)
            else:
                de_p_f(sentence) 
        
        else:
            hash_value = sentence_tuple[1]
            
            if sentence_tuple[0] == 'R':
                file = sentence_tuple[1]
                print(f"Received a response message from peer{sou_peer}, which has the file{file}.")
            else:
                file =  sentence_tuple[2]
                TCP_pe_number = sou_addr[1]-60000
                
                request_peer = sentence_tuple[0]
                request_port = sentence_tuple[0]+50000
                

                if TCP_pe_number < hash_value <= arg1 or TCP_pe_number > arg1 and hash_value > TCP_pe_number:
                    print(f"File {file} is here")
                    new_c_so(request_port,file)
                else:
                    print(f"File {file} is not stored here")
                    new_c_s(sentence)
        connect_s.close()

        
        

def main():

    TCP_thread_s = threading.Thread(target=thread_job_s)
    UDP_thread = threading.Thread(target=UDP_thread_job)
    TCP_thread_c = threading.Thread(target=thread_job_c)
    
    
    TCP_thread_s.start()
    TCP_thread_c.start()
    UDP_thread.start()
    

main()
