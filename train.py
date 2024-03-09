from model.unet_model import UNet
from utils.dataset import UnetDataset
from torch import optim
import torch.nn as nn
import torch

def train_net(net,device,data_path,epochs=400,batch_size=1,lr=0.00001):
    #准备数据
    dataset = UnetDataset(data_path)
    train_loader = torch.utils.data.DataLoader(dataset,batch_size=batch_size,shuffle=True)
    #定义损失函数和优化器
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(net.parameters(),lr=lr,weight_decay=1e-8)
    # optimizer=optim.RMSprop(net.parameters(),lr=lr,weight_decay=1e-8,alpha=0.9)
    best_loss = float('inf')
    #开始训练
    for epoch in range(epochs):
        net.train()
        for img,label in train_loader:
            img = img.to(device=device,dtype=torch.float32)
            label = label.to(device=device,dtype=torch.float32)
            #前向传播
            logits = net(img)
            #计算损失
            loss = criterion(logits,label)
            print("Loss: {:.4f}".format(loss.item()))

            if loss < best_loss:
                best_loss = loss
                torch.save(net.state_dict(),'best_model.pth')
            #梯度清零
            optimizer.zero_grad()
            #反向传播
            loss.backward()
            #更新权重
            optimizer.step()
        print("Epoch [{}/{}], Loss: {:.4f}".format(epoch+1,epochs,loss.item()))

if __name__ == "__main__":

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    net = UNet(n_channels=1,n_classes=1)

    net.to(device=device)
    train_net(net,device,'data/train/')