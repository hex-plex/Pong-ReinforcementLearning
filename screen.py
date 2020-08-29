import numpy as np
import cv2
from mss import mss
from PIL import Image

rgb2bgr= lambda x: np.append(np.append(x[:,:,2].reshape([x.shape[0],x.shape[1],1]),x[:,:,1].reshape([x.shape[0],x.shape[1],1]),axis=2),x[:,:,0].reshape([x.shape[0],x.shape[1],1]),axis=2)

mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
flag=0
vid_flag=False
sct = mss()
t=1
img_buff = []
while t>0:
    sct.get_pixels(mon)
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    if flag>0:
        if flag>5:
            img_buff.append(rgb2bgr(cv2.resize(np.array(img),(800,450))))
        else:
            flag+=1
    ##cv2.imwrite('/home/hexplex0xff/ass/output'+str(t)+".jpg",rgb2bgr(np.array(img)))
    cv2.imshow('test', rgb2bgr(np.array(img)))
    t+=1
    k =cv2.waitKey(100)
    if  k&0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    elif k&0xFF == ord('s'):
        flag=1
    elif k&0xFF == ord('d'):
        flag = 0
        vid_flag = True
        break
    elif k&0xFF == ord('n'):
        flag = 0
        break
if vid_flag:
    out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'),10,(800,450))
    for i in range(len(img_buff)-5):
        out.write(img_buff[i])
    out.release()
