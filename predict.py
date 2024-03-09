import glob
import os
import cv2
import torch
import numpy as np
from model.unet_model import UNet

if __name__ == "__main__":
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    net = UNet(n_channels=1,n_classes=1)
    net.to(device=device)
    net.load_state_dict(torch.load('best_model.pth',map_location=device))
    net.eval()

    data_path = 'data/test/'
    imgs_path = glob.glob(os.path.join(data_path,'*.png'))
    for img_path in imgs_path:

        save_res_path= img_path.split('.')[0]+"_res.png"
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img = img.reshape(1,1,img.shape[0],img.shape[1])
        
        img_tensor= torch.from_numpy(img)
        img_tensor = img_tensor.to(device=device,dtype=torch.float32)

        pred=net(img_tensor)
        pred=np.array(pred.data.cpu()[0])[0]

        pred[pred>0.5]=255
        pred[pred<=0.5]=0
        cv2.imwrite(save_res_path,pred)
