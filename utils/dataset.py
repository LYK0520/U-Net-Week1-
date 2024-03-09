import torch
import cv2
import os
import glob
from torch.utils.data import Dataset
import random

class UnetDataset(Dataset):
    def __init__(self,data_path):
        #初始化函数，读取所有data_path下的图片
        self.data_path = data_path
        self.imgs_path = glob.glob(os.path.join(data_path,'image/*.png'))

    def augment(selg,image,flipCode):
        #图像增强
        # cv2.flip(image,flipCode)是指对图像进行翻转，flipCode=0表示绕x轴翻转，flipCode=1表示绕y轴翻转，flipCode=-1表示绕x轴和y轴翻转
        image = cv2.flip(image,flipCode)
        return image

    def __getitem__(self,index):
        #根据index读取图片
        img_path = self.imgs_path[index]
        label_path = img_path.replace('image','label')
        #读取训练图片和标签图片
        img = cv2.imread(img_path)
        label= cv2.imread(label_path)

        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        label=cv2.cvtColor(label,cv2.COLOR_BGR2GRAY)

        img=img.reshape(1,img.shape[0],img.shape[1])
        label=label.reshape(1,label.shape[0],label.shape[1])

        if label.max()>1:
            label = label/255

        flipCode = random.choice([0,1,-1])
        if flipCode != 0:
            img = self.augment(img,flipCode)
            label = self.augment(label,flipCode)

        return img,label

    def __len__(self):
        #返回训练集大小
        return len(self.imgs_path)

if __name__ == "__main__":
    UnetDataset = UnetDataset('data/train/')
    print(UnetDataset.__len__())

    train_loader = torch.utils.data.DataLoader(UnetDataset,batch_size=200,shuffle=True)

    for img,label in train_loader:
        print(img.shape)
        print(label.shape)
        break