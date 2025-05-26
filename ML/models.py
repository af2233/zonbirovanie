import torch
from torch import nn
import torchvision
import torch.nn.functional as F
from torchvision import transforms
from typing import Tuple
from pathlib import Path


class BasicBlock(nn.Module):
    expansion = 1
    def __init__(self, in_planes, planes, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)

        self.downsample = None
        if stride != 1 or in_planes != planes:
            self.downsample = nn.Sequential(
                nn.Conv2d(in_planes, planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(planes)
            )

    def forward(self, x):
        identity = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)
        return out

class CustomResNetFCN(nn.Module):
    def __init__(self, block, layers, out_channels=3):
        super().__init__()
        self.in_planes = 64
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.layer1 = self._make_layer(block, 64, 2, stride=1)
        self.layer2 = self._make_layer(block, 128, 2, stride=2)
        self.layer3 = self._make_layer(block, 256, 2, stride=2)
        self.layer4 = self._make_layer(block, 512, 2, stride=2)

        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(512, 256, kernel_size=4, stride=2, padding=1),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(64, out_channels, kernel_size=4, stride=2, padding=1),
        )

    def _make_layer(self, block, planes, blocks, stride):
        layers = []
        layers.append(block(self.in_planes, planes, stride))
        self.in_planes = planes * block.expansion
        for _ in range(1, blocks):
            layers.append(block(self.in_planes, planes))
        return nn.Sequential(*layers)

    def forward(self, x):
        input_size = x.shape[2:]
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.decoder(x)
        x = F.interpolate(x, size=input_size, mode='bilinear', align_corners=False)
        return x



class UNet(nn.Module):
    def __init__(self, dropout=0.2):
        super().__init__()

        self.backbone = CustomResNetFCN(BasicBlock, [2, 2, 2, 2], out_channels=3)

        self.pool = nn.MaxPool2d(2, 2)

        # Encoder (downsampling path)
        self.encode1 = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            # nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1),
            # nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        self.encode2 = nn.Sequential(
            nn.Conv2d(32, 64, 3, padding=1),
            # nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1),
            # nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        self.encode3 = nn.Sequential(
            nn.Conv2d(64, 128, 3, padding=1),
            # nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1),
            # nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        self.encode4 = nn.Sequential(
            nn.Conv2d(128, 256, 3, padding=1),
            # nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1),
            # nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        self.encode5 = nn.Sequential(
            nn.Conv2d(256, 512, 3, padding=1),
            # nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Conv2d(512, 512, 3, padding=1),
            # nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Dropout(dropout)
        )

        # Bottleneck
        self.bottleneck = nn.Sequential(
            nn.Conv2d(512, 1024, 3, padding=1),
            # nn.BatchNorm2d(1024),
            nn.ReLU(),
            nn.Conv2d(1024, 1024, 3, padding=1),
            # nn.BatchNorm2d(1024),
            nn.ReLU(),
            nn.Dropout(dropout)
        )

        # Decoder (upsampling path)
        self.upconv1 = nn.ConvTranspose2d(1024, 512, 2, stride=2)
        self.decode1 = nn.Sequential(
            nn.Conv2d(1024, 512, 3, padding=1),
            # nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Conv2d(512, 512, 3, padding=1),
            # nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        self.upconv2 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.decode2 = nn.Sequential(
            nn.Conv2d(512, 256, 3, padding=1),
            # nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1),
            # nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        self.upconv3 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.decode3 = nn.Sequential(
            nn.Conv2d(256, 128, 3, padding=1),
            # nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1),
            # nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        self.upconv4 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.decode4 = nn.Sequential(
            nn.Conv2d(128, 64, 3, padding=1),
            # nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1),
            # nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        self.upconv5 = nn.ConvTranspose2d(64, 32, 2, stride=2)
        self.decode5 = nn.Sequential(
            nn.Conv2d(64, 32, 3, padding=1),
            # nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1),
            # nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Conv2d(32, 3, 1)  # Output layer
        )

    def forward(self, x):
        x = self.backbone(x)
    
        e1 = self.encode1(x)          # 320x320 -> 32 channels
        e2 = self.encode2(self.pool(e1))  # 160x160 -> 64 channels
        e3 = self.encode3(self.pool(e2))  # 80x80 -> 128 channels
        e4 = self.encode4(self.pool(e3))  # 40x40 -> 256 channels
        e5 = self.encode5(self.pool(e4))  # 20x20 -> 512 channels

        # Bottleneck
        bottle = self.bottleneck(self.pool(e5))  # 10x10 -> 1024 channels

        d1 = self.upconv1(bottle)      # 20x20
        d1 = torch.cat([d1, e5], dim=1)
        d1 = self.decode1(d1)          # 20x20 -> 512 channels
        
        d2 = self.upconv2(d1)          # 40x40
        d2 = torch.cat([d2, e4], dim=1)
        d2 = self.decode2(d2)          # 40x40 -> 256 channels
        
        d3 = self.upconv3(d2)          # 80x80
        d3 = torch.cat([d3, e3], dim=1)
        d3 = self.decode3(d3)          # 80x80 -> 128 channels
        
        d4 = self.upconv4(d3)          # 160x160
        d4 = torch.cat([d4, e2], dim=1)
        d4 = self.decode4(d4)          # 160x160 -> 64 channels
        
        d5 = self.upconv5(d4)          # 320x320
        d5 = torch.cat([d5, e1], dim=1)
        output = self.decode5(d5)      # 320x320 -> 3 channels (output)

        return output


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

# MODELS_PATH = Path('models')
# CHECKOPOINT = MODELS_PATH / 'model_45_mln_52_iou.pth'


# unet_model = UNet(dropout=0.2).to('cuda')
# unet_model.load_state_dict(torch.load(f='models/model_45_mln_52_iou.pth', map_location='cuda', weights_only=True))