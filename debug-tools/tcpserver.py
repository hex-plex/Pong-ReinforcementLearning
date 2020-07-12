import socket
import cv2
from io import BytesIO
import numpy as np
cv2.imshow('asdfasdf',cv2.imread('pong-game.png')[:300,:200,:])
cv2.waitKey(0)
cv2.destroyAllWindows()
def server():
  #host = socket.gethostname()   # get local machine name
  port = 18000  # Make sure it's within the > 1024 $$ <65535 range

  s = socket.socket()
  s.bind(('', port))

  s.listen(1)
  client_socket, adress = s.accept()
  print("Connection from: " + str(adress))
  while True:
    data = client_socket.recv(1024).decode('utf-8')
    if data=='m':
        print("INside")
        img=cv2.imread('pong-game.png')
        img = img[:300,:200,:]
        f = BytesIO()
        np.savez_compressed(f, frame=img)
        f.seek(0)
        out = f.read()
        client_socket.sendall(out)
        #client_socket.send(b'')
        print('hello')
    if not data:
      break
    print('From online user: ' + data)
    data = data.upper()
    client_socket.send(data.encode('utf-8'))
  client_socket.close()
  s.close()

if __name__ == '__main__':
    server()
