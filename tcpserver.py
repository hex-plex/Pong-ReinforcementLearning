import socket

def server():
  #host = socket.gethostname()   # get local machine name
  port = 18000  # Make sure it's within the > 1024 $$ <65535 range

  s = socket.socket()
  s.bind(('192.168.1.6', port))

  s.listen(1)
  client_socket, adress = s.accept()
  print("Connection from: " + str(adress))
  while True:
    data = client_socket.recv(1024).decode('utf-8')
    if not data:
      break
    print('From online user: ' + data)
    data = data.upper()
    client_socket.send(data.encode('utf-8'))
  client_socket.close()
  s.close()

if __name__ == '__main__':
    server()
