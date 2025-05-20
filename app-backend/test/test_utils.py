from pathlib import Path
import torch
import os
import sys
from typing import Optional
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import get_embedding, cosine_distance, euclidean_distance

# Image paths
img1_path: str = 'test/src/20918356-0.jpg'
img2_path: str = 'test/src/Foto_Patricio.jpg'

# Read images as bytes
img1_bytes: bytes = Path(img1_path).read_bytes()
img2_bytes: bytes = Path(img2_path).read_bytes()

def main() -> None:
    """
    Main function to compute embeddings of two images and compare their similarity using
    cosine and euclidean distances.
    """
    try:
        # Get embeddings
        emb1: Optional[torch.Tensor] = get_embedding(img1_bytes, save_path='test/src/outputs/test_utils_DB_face.jpg')
        emb2: Optional[torch.Tensor] = get_embedding(img2_bytes, save_path='test/src/outputs/test_utils_Uploaded_face2.jpg')

        if emb1 is None or emb2 is None:
            raise ValueError("Face not detected in one or both images.")

        # Calculate distances
        cos_dist: float = cosine_distance(emb1, emb2)
        euc_dist: float = euclidean_distance(emb1, emb2)

        # Print results
        print(f'Cosine distance:     {cos_dist:.4f}')
        print(f'Euclidean distance:  {euc_dist:.4f}')

        # Interpretation
        if cos_dist < 0.5:
            print("Same face (cosine)")
        else:
            print("Different faces (cosine)")

        if euc_dist < 1.0:
            print("Same face (euclidean)")
        else:
            print("Different faces (euclidean)")

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()