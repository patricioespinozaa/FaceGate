from facenet_pytorch import InceptionResnetV1, MTCNN
import torch

# Load the pre-trained InceptionResnetV1 model for face recognition
model = InceptionResnetV1(pretrained='vggface2').eval()
# Initialize the face recognition model
mtcnn = MTCNN(
    image_size=224,             # Input image size
    margin=20,                  # Capture a bit more of the face
    select_largest=True,        # Select the largest face
    post_process=True,          # Post-process image after detection
    keep_all=False,             # Keep all detected faces
    device='cuda' if torch.cuda.is_available() else 'cpu'
)