# -*- coding: utf-8 -*-
import io
from typing import Optional
from PIL import Image
import torch
import torch.nn.functional as F
from facenet_pytorch import MTCNN
from app import model
from torchvision.transforms import ToPILImage


# Initialize the face recognition model
mtcnn = MTCNN(
    image_size=224,             # Input image size
    margin=20,                  # Capture a bit more of the face
    select_largest=True,        # Select the largest face
    post_process=True,          # Post-process image after detection
    keep_all=False,             # Keep all detected faces
    device='cuda' if torch.cuda.is_available() else 'cpu'
)

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

def cosine_distance(a: torch.Tensor, b: torch.Tensor) -> float:
    """
    Compute the cosine distance between two embeddings.

    Args:
        a (torch.Tensor): First embedding tensor.
        b (torch.Tensor): Second embedding tensor.

    Returns:
        float: Cosine distance between a and b.
    """
    return 1 - F.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0)).item()

def euclidean_distance(a: torch.Tensor, b: torch.Tensor) -> float:
    """
    Compute the Euclidean distance between two embeddings.

    Args:
        a (torch.Tensor): First embedding tensor.
        b (torch.Tensor): Second embedding tensor.

    Returns:
        float: Euclidean distance between a and b.
    """
    return torch.norm(a - b).item()
