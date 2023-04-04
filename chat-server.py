import socket
import datetime
import threading
import json
import sys

PORT = 7500
BUFSIZE = 4096
SERVERIP = '0.0.0.0'

clientList = []
clientDict = {}
    

def clientHandler(client, addr):
  while True:
    try:
      data =client.recv(BUFSIZE)
      check = data.decode('utf-8').split('|')
      if check[0] == 'NAME':
        clientDict[str(addr)] = check[1]
    except:
      clientList.remove(client)
      break

    if (not data) or (data.decode('utf-8') == 'q'):
      getname = clientDict[str(addr)]
      clientList.remove(client)
      print('OUT : ', getname)
      print('Count Users : ', len(clientList))
      break
    # for name in clientDict:
    check = data.decode('utf-8').split('|')
    getname = clientDict[str(addr)]
    if check[0] == 'NAME':
      msg = getname + ' Join' + '\n'
    else:
      msg = getname + ' : ' + data.decode('utf-8') + '\n'
    print(msg)
    for c in clientList:
      c.sendall(msg.encode('utf-8'))
  
  client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVERIP, PORT))
server.listen(5)

if __name__ == '__main__':
  while True:
    client, addr = server.accept()
    clientList.append(client)
    print('Count Users : ', len(clientList))

    task = threading.Thread(target = clientHandler, args = (client, addr))
    task.start()