import torch
from torchvision import transforms
from PIL import Image
import io
import json

class DiseasePredictor:
    def __init__(self, model_path: str, class_names_path: str = "models/class_names.json"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model(model_path)
        self.class_names = self._load_classes(class_names_path)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def _load_model(self, path: str):
        from model import PlantDiseaseModel
        model = PlantDiseaseModel(num_classes=38)
        model.load_state_dict(torch.load(path, map_location=self.device))
        model.to(self.device)
        model.eval()
        return model

    def _load_classes(self, path: str) -> list:
        with open(path, "r") as f:
            return json.load(f)

    def predict(self, image_bytes: bytes) -> dict:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(tensor)
            probs = torch.softmax(outputs, dim=1)
            confidence, idx = torch.max(probs[0], 0)

        class_name = self.class_names[idx.item()]
        parts = class_name.split("___")
        crop = parts[0] if len(parts) > 1 else "Unknown"
        disease = parts[1].replace("_", " ").title() if len(parts) > 1 else "Healthy"

        return {
            "crop": crop,
            "disease": disease,
            "confidence": round(confidence.item(), 4),
            "class_name": class_name,
            "top_3": [
                {"label": self.class_names[i], "prob": round(p, 4)}
                for p, i in zip(*torch.topk(probs[0], 3))
            ]
        }
