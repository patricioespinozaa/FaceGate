# -*- coding: utf-8 -*-
import io
from app import model, imagenet_class_index
import torchvision.transforms as transforms
from PIL import Image
import torch.nn.functional as F

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(256, interpolation=transforms.InterpolationMode.BILINEAR),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

def get_prediction(image_bytes):
    print("evaluando imagen en la red...")
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    probabilities = F.softmax(outputs, dim=1)

    # Obtener las 3 clases con mayor probabilidad
    topk_scores, topk_indices = probabilities.topk(3, dim=1)

    resultados = []
    for i in range(3):
        score = round(topk_scores[0][i].item(), 4)
        class_id = topk_indices[0][i].item()
        class_name = imagenet_class_index[str(class_id)][1]
        resultados.append({'score': score, 'clase_id': class_id, 'clase_nombre': class_name})
        print(f"Top-{i+1}: {score} - {class_id} - {class_name}")

    return resultados