import socket
import datetime
import threading
import json

PORT = 7500
BUFSIZE = 4096
SERVERIP = '0.0.0.0'

clientList = []

def clientHandler(client, addr):
  while True:
    try:
      data =client.recv(BUFSIZE)
    except:
      clientList.remove(client)
      break

    if (not data) or (data.decode('utf-8') == 'q'):
      clientList.remove(client)
      print('OUT : ', client)
      print('Count Users : ', len(clientList))
      break
    msg = str(addr) + '>>>' + data.decode('utf-8') + '\n'
    print('USER : ', msg)
    print('--------------')
    for c in clientList:
      c.sendall(msg.encode('utf-8'))
  
  client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVERIP, PORT))
server.listen(5)

while True:
  client, addr = server.accept()
  clientList.append(client)
  print('Count Users : ', len(clientList))

  task = threading.Thread(target = clientHandler, args = (client, addr))
  task.start()