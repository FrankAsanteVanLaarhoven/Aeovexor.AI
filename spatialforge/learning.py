"""3D Deep Learning Neural Architectures for SpatialForge-3D.

PyTorch implementations of:
- PointNetLite: End-to-end 3D point cloud classification and semantic segmentation network
- Feature embedding encoder
- Multi-class point-wise inference and evaluation pipelines
"""
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class PointNetLite(nn.Module):
    """Lightweight and highly efficient PointNet architecture for 3D perception.
    
    Supports both global point cloud classification and dense per-point semantic segmentation.
    Input tensor: (Batch, Channels, NumPoints) where Channels >= 3 (XYZ + optional intensity/normals).
    """

    def __init__(self, in_channels: int = 3, num_classes: int = 19, mode: str = "segmentation"):
        super().__init__()
        self.in_channels = in_channels
        self.num_classes = num_classes
        self.mode = mode

        # Shared Point-wise MLPs (Implemented via 1D Convolutions)
        self.conv1 = nn.Conv1d(in_channels, 64, 1)
        self.conv2 = nn.Conv1d(64, 128, 1)
        self.conv3 = nn.Conv1d(128, 512, 1)

        self.bn1 = nn.BatchNorm1d(64)
        self.bn2 = nn.BatchNorm1d(128)
        self.bn3 = nn.BatchNorm1d(512)

        if mode == "classification":
            self.fc1 = nn.Linear(512, 256)
            self.fc2 = nn.Linear(256, 128)
            self.fc3 = nn.Linear(128, num_classes)
            self.dropout = nn.Dropout(p=0.3)
        else:
            # Segmentation Head: Combines point features (64) + global feature (512) = 576 channels
            self.seg_conv1 = nn.Conv1d(512 + 64, 256, 1)
            self.seg_conv2 = nn.Conv1d(256, 128, 1)
            self.seg_conv3 = nn.Conv1d(128, num_classes, 1)

            self.seg_bn1 = nn.BatchNorm1d(256)
            self.seg_bn2 = nn.BatchNorm1d(128)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass.
        
        Args:
            x: Tensor of shape (B, C, N)
        Returns:
            If mode == 'classification': (B, num_classes) logits
            If mode == 'segmentation': (B, num_classes, N) per-point logits
        """
        B, C, N = x.shape

        # Point feature extraction
        out1 = F.relu(self.bn1(self.conv1(x)))  # (B, 64, N)
        out2 = F.relu(self.bn2(self.conv2(out1)))  # (B, 128, N)
        out3 = F.relu(self.bn3(self.conv3(out2)))  # (B, 512, N)

        # Global feature aggregation (Max Pooling over all points)
        global_feat = torch.max(out3, 2, keepdim=True)[0]  # (B, 512, 1)

        if self.mode == "classification":
            flat = global_feat.view(B, -1)
            f = F.relu(self.fc1(flat))
            f = self.dropout(F.relu(self.fc2(f)))
            return self.fc3(f)
        else:
            # Replicate global feature across all N points and concatenate
            global_repeat = global_feat.repeat(1, 1, N)  # (B, 512, N)
            combined = torch.cat([out1, global_repeat], dim=1)  # (B, 576, N)

            s1 = F.relu(self.seg_bn1(self.seg_conv1(combined)))
            s2 = F.relu(self.seg_bn2(self.seg_conv2(s1)))
            logits = self.seg_conv3(s2)  # (B, num_classes, N)
            return logits


def predict_point_semantics(
    model: nn.Module,
    xyz: np.ndarray,
    features: Optional[np.ndarray] = None,
    device: str = "cpu",
) -> np.ndarray:
    """Runs semantic segmentation inference on an arbitrary-sized point cloud.
    
    Subsamples into blocks of up to 4096 points for batch inference.
    Returns:
        predicted_classes: (N,) int32 array of class predictions
    """
    model.eval()
    xyz = np.asarray(xyz, dtype=np.float32)
    n = len(xyz)
    if n == 0:
        return np.empty(0, dtype=np.int32)

    if features is not None:
        feat = np.asarray(features, dtype=np.float32)
        in_data = np.hstack([xyz, feat])
    else:
        in_data = xyz

    block_size = 4096
    predictions = np.zeros(n, dtype=np.int32)

    with torch.no_grad():
        for i in range(0, n, block_size):
            chunk = in_data[i : i + block_size]
            c_len = len(chunk)
            # Pad chunk if smaller than block_size
            if c_len < block_size:
                pad = np.repeat(chunk[-1:], block_size - c_len, axis=0)
                padded_chunk = np.vstack([chunk, pad])
            else:
                padded_chunk = chunk

            # (1, C, block_size)
            tensor_in = torch.from_numpy(padded_chunk.T).unsqueeze(0).to(device)
            logits = model(tensor_in)  # (1, num_classes, block_size)
            preds = torch.argmax(logits, dim=1).squeeze(0).cpu().numpy()
            predictions[i : i + c_len] = preds[:c_len]

    return predictions
