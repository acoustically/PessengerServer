from socket import *
from select import select
import sys
import json

from SocketReadThread import *
import SocketWriteThread

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(("", 8100))
server_socket.listen(5)
#TODO : maintain client socket classified by phone number
client_socket_list = [];

while(1):
  print("socket wait")
  client_socket, client_address = server_socket.accept() 
  print("socket accepted - " + client_address[0] + ":" + str(client_address[1]) + " is accepted")
  socket_read_thread = SocketReadThread(client_socket, client_socket_list);
  socket_read_thread.start()
