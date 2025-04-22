import torch
from torch import nn
import torchvision
from torchvision import transforms
from typing import Tuple


class UNet(nn.Module):
    def __init__(self, dropout: int):
        super().__init__()
        self.pool = nn.MaxPool2d(2, 2)

        self.encode1 = nn.Sequential( # (3, 256, 256) + pool -> (16, 128, 128) 
            nn.Conv2d(3, 16, 3, 1, 1),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Conv2d(16, 16, 3, 1, 1),
            nn.ReLU(),
        )

        self.encode2 = nn.Sequential( # (16, 128, 128)  -> (32, 64, 64) 
            nn.Conv2d(16, 32, 3, 1, 1),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Conv2d(32, 32, 3, 1, 1),
            nn.ReLU(),
        )

        self.encode3 = nn.Sequential( # (32, 64, 64) -> (64, 32, 32)
            nn.Conv2d(32, 64, 3, 1, 1),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Conv2d(64, 64, 3, 1, 1),
            nn.ReLU(),
        )

        self.encode4 = nn.Sequential( # (64, 32, 32) -> (128, 16, 16)
            nn.Conv2d(64, 128, 3, 1, 1),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Conv2d(128, 128, 3, 1, 1),
            nn.ReLU(),
        )

        self.encode5 = nn.Sequential( # (128, 16, 16) -> (256, 8, 8)
            nn.Conv2d(128, 256, 3, 1, 1),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Conv2d(256, 256, 3, 1, 1),
            nn.ReLU(),
        )

        self.bottleneck = nn.Sequential( # (256, 8, 8) -> (256, 8, 8) -> (256, 8, 8)
            nn.Conv2d(256, 256, 3, 1, 1),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Conv2d(256, 256, 3, 1, 1),
            nn.ReLU(),
            nn.Upsample(16),
            nn.Conv2d(256, 256, 3, 1, 1),
            nn.ReLU()
        )
        self.decode1 = nn.Sequential( # (512, 8, 8) -> (128, 16, 16)
            nn.Conv2d(512, 256, 3, 1, 1),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Conv2d(256, 256, 3, 1, 1),
            nn.ReLU(),
            nn.Upsample(32),
            nn.Conv2d(256, 128, 3, 1, 1),
            nn.ReLU()
        )
        self.decode2 = nn.Sequential( # (128, 16, 16) -> (64, 32, 32)
            nn.Conv2d(256, 128, 3, 1, 1),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Conv2d(128, 128, 3, 1, 1),
            nn.ReLU(),
            nn.Upsample(64),
            nn.Conv2d(128, 64, 3, 1, 1),
            nn.ReLU()
        )
        self.decode3 = nn.Sequential( # (128, 32, 32) -> (32, 64, 64)
            nn.Conv2d(128, 64, 3, 1, 1),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Conv2d(64, 64, 3, 1, 1),
            nn.ReLU(),
            nn.Upsample(128),
            nn.Conv2d(64, 32, 3, 1, 1),
            nn.ReLU()
        )
        self.decode4 = nn.Sequential( # (64, 64, 64) -> (16, 128, 128)
            nn.Conv2d(64, 32, 3, 1, 1),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Conv2d(32, 32, 3, 1, 1),
            nn.ReLU(),
            nn.Upsample(256),
            nn.Conv2d(32, 16, 3, 1, 1),
            nn.Dropout(dropout),
            nn.Conv2d(16, 16, 3, 1, 1),
            nn.ReLU(),
            nn.Conv2d(16, 3, 3, 1, 1),
            nn.ReLU()

        )


    def forward(self, x):
        # encoding
        e1 = self.encode1(x)
        e2 = self.encode2(self.pool(e1))
        e3 = self.encode3(self.pool(e2))
        e4 = self.encode4(self.pool(e3))
        e5 = self.encode5(self.pool(e4))

        #bottleneck
        bottle = self.bottleneck(e5)


        #decoding
        d1 = self.decode1(torch.cat((bottle, e5), 1))
        d2 = self.decode2(torch.cat((d1, e4), 1))
        d3 = self.decode3(torch.cat((d2, e3), 1))
        d4 = self.decode4(torch.cat((d3, e2), 1))

        return d4
    

def get_transforms(img_size: int) -> Tuple[transforms.Compose, transforms.Compose]:
    X_trans = transforms.Compose([ 
        transforms.Resize(size=(img_size, img_size)),
        transforms.ToTensor()
        ])

    y_trans = transforms.Compose([
        transforms.Resize(size=(img_size, img_size)),
        transforms.ToTensor()
        ])
    
    return X_trans, y_trans