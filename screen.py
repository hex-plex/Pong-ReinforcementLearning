import numpy as np
import cv2
from mss import mss
from PIL import Image

rgb2bgr= lambda x: np.append(np.append(x[:,:,2].reshape([x.shape[0],x.shape[1],1]),x[:,:,1].reshape([x.shape[0],x.shape[1],1]),axis=2),x[:,:,0].reshape([x.shape[0],x.shape[1],1]),axis=2)

mon = {'top': 50, 'left': 640, 'width': 730, 'height': 530}

sct = mss()
t=1
while t>0:
    sct.get_pixels(mon)
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    cv2.imwrite('output/output'+str(t)+".jpg",rgb2bgr(np.array(img)))
    cv2.imshow('test', rgb2bgr(np.array(img)))
    t+=1
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
