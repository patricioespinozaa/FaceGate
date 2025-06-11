import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import io
from PIL import Image
from torchvision.transforms import ToPILImage
import torch
from models.face_model import model, mtcnn
from typing import Optional

def get_embedding(image_bytes: bytes, save_path: Optional[str] = None) -> Optional[torch.Tensor]:
    """
    Extract the face embedding from image bytes.

    Args:
        image_bytes (bytes): Image data in bytes.
        save_path (Optional[str]): Optional path to save the cropped face image.

    Returns:
        Optional[torch.Tensor]: The embedding tensor if a face is detected, else None.
    """
    # Read and convert image to RGB
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

    # Detect face
    face = mtcnn(image)
    if face is None:
        return None

    # Optionally save the detected face image
    if save_path is not None:
        pil_face = ToPILImage()(face)  # Convert tensor to PIL image
        pil_face.save(save_path)       # Save to specified path

    # Prepare face tensor for model
    face = face.unsqueeze(0)

    # Get embedding without gradient calculation
    with torch.no_grad():
        embedding = model(face)

    return embedding.squeeze(0)