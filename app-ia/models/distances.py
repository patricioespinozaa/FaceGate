import torch
import torch.nn.functional as F

def cosine_distance(a: torch.Tensor, b: torch.Tensor) -> float:
    """
    Compute the cosine distance between two embeddings.

    Args:
        a (torch.Tensor): First embedding tensor.
        b (torch.Tensor): Second embedding tensor.

    Returns:
        float: Cosine distance between a and b.
    """
    if isinstance(a, list):
        a = torch.tensor(a, dtype=torch.float32)
    if isinstance(b, list):
        b = torch.tensor(b, dtype=torch.float32)
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
    if isinstance(a, list):
        a = torch.tensor(a, dtype=torch.float32)
    if isinstance(b, list):
        b = torch.tensor(b, dtype=torch.float32)
    return torch.norm(a - b).item()


def tensor_to_list_dict(d: dict) -> dict:
    """
    Converts tensor-type values in a dictionary to standard Python lists.

    Args:
        d (dict): Dictionary with values that may be tensors.

    Returns:
        dict: Dictionary with values converted to lists.
    """
    return {
        k: v.tolist() if hasattr(v, 'tolist') else v
        for k, v in d.items()
    }