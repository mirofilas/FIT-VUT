#xfilas00

import argparse
import re

import os
import sys
import socket
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM #tento line asi netreba



parser = argparse.ArgumentParser()
parser.add_argument('-n')
parser.add_argument('-f')

args = parser.parse_args()

nameserver_regex = re.compile(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{1,5}$')
surl_regex = re.compile(r'^fsp:\/\/[a-zA-Z0-9\-\_\.]+\/.+$')

nameserver = nameserver_regex.match(args.n)
surl = surl_regex.match(args.f)

if(nameserver and surl):
    nameserver = nameserver.group(0)
    surl = surl.group(0)
else:
    sys.exit("Invalid arguments")

#zistenie ip servera cez nsp pre fsp
nameserver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
nameserver_ip, sep, nameserver_port = nameserver.partition(':')

fsp, sep, url_nsp_and_path = surl.partition('://')
whereis_nsp_hostname, sep, path = url_nsp_and_path.partition('/') 

whereis_msg = "WHEREIS " + whereis_nsp_hostname
nameserver_socket.sendto(whereis_msg.encode(), (nameserver_ip, int(nameserver_port)))
nameserver_socket.settimeout(30)
try:
    message, nsp_client_address = nameserver_socket.recvfrom(2048)
except socket.timeout:
    nameserver_socket.close()
    sys.exit("udp timed out")
nameserver_socket.close()
#v message je ip:port fileserveru
message = message.decode()
return_code, sep, ip_address = message.partition(' ')

if(return_code != "OK"):
    sys.exit("Nameserver return message error")
else:
    #nameserver ip je validna
    fileserver_ip, sep, fileserver_port = ip_address.partition(':')
    
    p, sep, write_file = path.rpartition('/')
    
    if(write_file == '*'):
        message_to_fileserver = "GET " + "index" + " FSP/1.0\r\n" + "Hostname: " + whereis_nsp_hostname + "\r\nAgent: xfilas00\r\n\r\n"
        fileserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fileserver_socket.connect((fileserver_ip, int(fileserver_port)))
        fileserver_socket.send(message_to_fileserver.encode())

        #vytvori buffer ako bytearray
        index_buffer = bytearray()
        while(1):
            message_from_fileserver = fileserver_socket.recv(1024)
            if not message_from_fileserver:
                break #EOF
            index_buffer.extend(message_from_fileserver)
          
        
        fileserver_socket.close()    
        recv = re.search(b"FSP/1.0 Success", index_buffer)
        if not recv:
            sys.exit("Fileserver index message error")
        #vymaze hlavicku
        index_buffer = index_buffer.split(b"\n", 3)[3]
        #rozdeli na medzery
        lines = index_buffer.decode().split('\r\n')

    else:
        index_buffer = path
        lines = index_buffer.split('\r\n')

    
    for file_name in lines:
        #preskoci prazdne riadky
        if not re.match(r'^\s*$', file_name):
        
            fileserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            fileserver_socket.connect((fileserver_ip, int(fileserver_port)))

            message_to_fileserver = "GET " + file_name + " FSP/1.0\r\n" + "Hostname: " + whereis_nsp_hostname + "\r\nAgent: xfilas00\r\n\r\n"
           
            fileserver_socket.send(message_to_fileserver.encode())
            

            index_buffer = bytearray()
            while(1):
                message_from_fileserver = fileserver_socket.recv(1024)
                if not message_from_fileserver:
                    break #EOF
                index_buffer.extend(message_from_fileserver)
            if not index_buffer:
                sys.exit("tcp connection problem")

            fileserver_socket.close()

            #vymaze hlavicku
            recv = re.search(b"FSP/1.0 Success", index_buffer)
            if not recv:
                sys.exit("Fileserver return message error")

            index_buffer = index_buffer.split(b"\n", 3)[3]
            pa, sep, name = file_name.rpartition('/')
            with open(name, 'wb+') as f:
                    f.write(index_buffer)  
            

        
