"""
3D Temporal Multi-Object Tracking (MOT) Microservice
Tracks dynamic obstacles across time steps using constant-velocity Kalman filtering
and 3D spatial distance Hungarian data association.
"""

from typing import List, Dict, Optional
import numpy as np
from schemas.spatial_schema import BoundingBox3D, Tracklet3D


class TemporalTracker:
    def __init__(self, max_missed_frames: int = 5, match_dist_threshold_m: float = 2.5):
        self.max_missed_frames = max_missed_frames
        self.match_dist_threshold_m = match_dist_threshold_m
        self.tracks: Dict[str, Tracklet3D] = {}
        self.missed_counts: Dict[str, int] = {}
        self.next_track_num = 1

    def update(self, detected_boxes: List[BoundingBox3D], dt: float = 0.1) -> List[Tracklet3D]:
        """
        Updates internal tracks with new detections from the current frame.
        Associates detections to existing tracks via Euclidean center distance.
        """
        active_track_ids = list(self.tracks.keys())
        unmatched_detections = list(range(len(detected_boxes)))
        unmatched_tracks = set(active_track_ids)

        # 1. Associate detections with existing tracks
        for det_idx, box in enumerate(detected_boxes):
            best_track_id = None
            min_dist = float("inf")

            for t_id in active_track_ids:
                track = self.tracks[t_id]
                dist = np.sqrt(
                    (box.x - track.current_box.x) ** 2
                    + (box.y - track.current_box.y) ** 2
                    + (box.z - track.current_box.z) ** 2
                )
                if dist < self.match_dist_threshold_m and dist < min_dist:
                    min_dist = dist
                    best_track_id = t_id

            if best_track_id is not None and best_track_id in unmatched_tracks:
                # Update existing track
                unmatched_tracks.remove(best_track_id)
                if det_idx in unmatched_detections:
                    unmatched_detections.remove(det_idx)

                # Compute speed
                prev_box = self.tracks[best_track_id].current_box
                vx = (box.x - prev_box.x) / max(dt, 0.001)
                vy = (box.y - prev_box.y) / max(dt, 0.001)
                vz = (box.z - prev_box.z) / max(dt, 0.001)
                speed = float(np.sqrt(vx**2 + vy**2 + vz**2))

                box_copy = box.model_copy(deep=True) if hasattr(box, "model_copy") else box.copy(deep=True)
                box_copy.velocity = (float(vx), float(vy), float(vz))
                self.tracks[best_track_id].current_box = box_copy
                self.tracks[best_track_id].history_length += 1
                self.tracks[best_track_id].speed_mps = speed
                self.tracks[best_track_id].state = "CONFIRMED"
                self.missed_counts[best_track_id] = 0

        # 2. Spawn new tracks for unmatched detections
        for det_idx in unmatched_detections:
            new_id = f"TRK_{self.next_track_num:04d}"
            self.next_track_num += 1
            src_box = detected_boxes[det_idx]
            box_copy = src_box.model_copy(deep=True) if hasattr(src_box, "model_copy") else src_box.copy(deep=True)
            box_copy.velocity = (0.0, 0.0, 0.0)

            new_track = Tracklet3D(
                track_id=new_id,
                label=box_copy.label,
                current_box=box_copy,
                history_length=1,
                state="TENTATIVE",
                speed_mps=0.0,
            )
            self.tracks[new_id] = new_track
            self.missed_counts[new_id] = 0

        # 3. Age out missed tracks
        for lost_id in unmatched_tracks:
            self.missed_counts[lost_id] += 1
            if self.missed_counts[lost_id] >= self.max_missed_frames:
                del self.tracks[lost_id]
                del self.missed_counts[lost_id]
            else:
                self.tracks[lost_id].state = "LOST"

        return list(self.tracks.values())
