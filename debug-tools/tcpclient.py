import socket
import cv2
from io import BytesIO
import numpy as np
def client():
  host = socket.gethostname()  # get local machine name
  port = 18000  # Make sure it's within the > 1024 $$ <65535 range

  s = socket.socket()
  s.connect((host, port))

  s.send('m'.encode('utf-8'))
  img_buffer=b''
  flag=True
  print(img_buffer)
  t=0
  inp_buffer=s.recv(4096)
  print('.')
  if not inp_buffer:
        return 1
  img_buffer += inp_buffer
  print("done")
  img=np.load(BytesIO(inp_buffer))['frame']
  cv2.imshow("asdf",img)
  cv2.waitKey(0)
  message = input('-> ')
  while message != 'q':
    s.send(message.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    print('Received from server: ' + data)
    message = input('==> ')
  s.close()

if __name__ == '__main__':client()
