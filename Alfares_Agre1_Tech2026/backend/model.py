import torch
import torch.nn as nn
from torchvision import models

class PlantDiseaseModel(nn.Module):
    """MobileNetV2 مع رأس تصنيف مخصص لـ 38 فئة أمراض نباتية"""

    def __init__(self, num_classes=38):
        super().__init__()
        self.backbone = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
        # استبدال الرأس الأخير
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(self.backbone.classifier[1].in_features, 128),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        return self.backbone(x)
