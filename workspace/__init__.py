"""SpatialForge-3D Workspace Package.

Provides high-performance FastAPI and WebSocket servers for the SpatialForge Studio
and Ouster-style LiDAR research console.
"""
from .server import app

__all__ = ["app"]
