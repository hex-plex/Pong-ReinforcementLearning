import socket

def client():
  #host = socket.gethostname()  # get local machine name
  port = 18000  # Make sure it's within the > 1024 $$ <65535 range

  s = socket.socket()
  s.connect(("192.168.1.6", port))

  message = input('-> ')
  while message != 'q':
    s.send(message.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    print('Received from server: ' + data)
    message = input('==> ')
  s.close()

if __name__ == '__main__':client()
