"""Sensor-neutral Multi-Format I/O Engine for SpatialForge-3D.

Pure Python / NumPy implementations with zero mandatory external C-library
dependencies, supporting:
- NumPy (.npy, .npz)
- KITTI LiDAR (.bin XYZI float32)
- SemanticKITTI (.label semantic/instance)
- Stanford PLY (ASCII & Binary Little-Endian)
- Point Cloud Library PCD (ASCII & Binary)
- ROS 2 sensor_msgs/PointCloud2 (binary CDR / byte buffer serializer & deserializer)
- ASPRS LAS LiDAR format (native record parser)
- Trajectories (KITTI 12-float and TUM timestamp-quaternion)
"""
import io
from pathlib import Path
import struct
from typing import Dict, Optional, Tuple, Union
import numpy as np
from scipy.spatial.transform import Rotation

from .contracts import FrameMetadata, SpatialFrame

# SemanticKITTI learning map (28 raw classes -> 19 learning classes)
SEMANTIC_KITTI_LEARNING_MAP = {
    0: 0,     # "unlabeled"
    1: 0,     # "outlier" mapped to "unlabeled"
    10: 1,    # "car"
    11: 2,    # "bicycle"
    13: 5,    # "bus" mapped to "other-vehicle"
    15: 3,    # "motorcycle"
    16: 5,    # "on-rails" mapped to "other-vehicle"
    18: 4,    # "truck"
    20: 5,    # "other-vehicle"
    30: 6,    # "person"
    31: 7,    # "bicyclist"
    32: 8,    # "motorcyclist"
    40: 9,    # "road"
    44: 10,   # "parking"
    48: 11,   # "sidewalk"
    49: 12,   # "other-ground"
    50: 13,   # "building"
    51: 14,   # "fence"
    52: 0,    # "other-structure" mapped to "unlabeled"
    70: 15,   # "vegetation"
    71: 16,   # "trunk"
    72: 17,   # "terrain"
    80: 18,   # "pole"
    81: 19,   # "traffic-sign"
    99: 0,    # "other-object"
    252: 1,   # "moving-car"
    253: 7,   # "moving-bicyclist"
    254: 6,   # "moving-person"
    255: 8,   # "moving-motorcyclist"
    256: 5,   # "moving-on-rails"
    257: 5,   # "moving-bus"
    258: 4,   # "moving-truck"
    259: 5,   # "moving-other-vehicle"
}

SEMANTIC_KITTI_CLASS_NAMES = [
    "unlabeled", "car", "bicycle", "motorcycle", "truck", "other-vehicle",
    "person", "bicyclist", "motorcyclist", "road", "parking", "sidewalk",
    "other-ground", "building", "fence", "vegetation", "trunk", "terrain",
    "pole", "traffic-sign"
]


def load_frame(
    path: Union[str, Path],
    fmt: str = "auto",
    labels_path: Optional[Union[str, Path]] = None,
    coordinate_frame: str = "sensor_lidar",
) -> SpatialFrame:
    """Loads a point cloud file into a canonical SpatialFrame."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")

    ext = p.suffix.lstrip(".").lower() if fmt == "auto" else fmt.lower()
    intensity = None
    rgb = None
    normals = None
    classes = None
    instances = None

    if ext == "npy":
        raw = np.load(p, allow_pickle=False)
        if raw.ndim != 2 or raw.shape[1] not in (3, 4, 6):
            raise ValueError(f"NPY point cloud must be (N, 3), (N, 4), or (N, 6), got {raw.shape}")
        xyz = raw[:, :3]
        if raw.shape[1] == 4:
            intensity = raw[:, 3]
        elif raw.shape[1] == 6:
            normals = raw[:, 3:6]

    elif ext == "npz":
        with np.load(p, allow_pickle=False) as f:
            if "xyz" in f:
                xyz = f["xyz"]
            elif "points" in f:
                xyz = f["points"]
            else:
                raise ValueError("NPZ must contain 'xyz' or 'points' array")
            intensity = f["intensity"] if "intensity" in f else None
            rgb = f["rgb"] if "rgb" in f else None
            normals = f["normals"] if "normals" in f else None
            classes = f["labels"] if "labels" in f else (f["classes"] if "classes" in f else None)
            instances = f["instances"] if "instances" in f else None

    elif ext in ("bin", "kitti", "velodyne"):
        xyz, intensity = read_kitti_velodyne(p)

    elif ext in ("tfrecord", "waymo") or p.name == "frames":
        frame_coord = coordinate_frame if coordinate_frame != "sensor_lidar" else "vehicle"
        return load_waymo_frame(p, coordinate_frame=frame_coord)

    elif ext == "ply":
        xyz, intensity, rgb, normals = read_ply(p)

    elif ext == "pcd":
        xyz, intensity, rgb, normals = read_pcd(p)

    elif ext in ("las", "laz"):
        xyz, intensity, rgb, classes = read_las(p)

    else:
        raise ValueError(f"Unsupported point cloud format: '{ext}'")

    if labels_path is not None:
        lp = Path(labels_path)
        if not lp.is_file():
            raise FileNotFoundError(f"Labels file not found: {lp}")
        raw_labels = np.fromfile(lp, dtype="<u4")
        if len(raw_labels) != len(xyz):
            raise ValueError(f"Label count ({len(raw_labels)}) != point count ({len(xyz)})")
        classes = (raw_labels & 0xFFFF).astype(np.int32)
        instances = (raw_labels >> 16).astype(np.int32)

    meta = FrameMetadata(
        coordinate_frame=coordinate_frame,
        sensor_id=p.stem,
        sensor_type="lidar" if ext in ("bin", "kitti", "las") else "general_3d",
    )

    return SpatialFrame(
        xyz=xyz,
        intensity=intensity,
        rgb=rgb,
        normals=normals,
        classes=classes,
        instances=instances,
        metadata=meta,
    )


def save_frame(frame: SpatialFrame, path: Union[str, Path], fmt: str = "auto") -> None:
    """Exports a SpatialFrame to disk in the chosen format."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    ext = p.suffix.lstrip(".").lower() if fmt == "auto" else fmt.lower()

    if ext == "npy":
        if frame.intensity is not None:
            data = np.hstack([frame.xyz, frame.intensity[:, None]])
        else:
            data = frame.xyz
        np.save(p, data)

    elif ext == "npz":
        arrays = {"xyz": frame.xyz}
        if frame.intensity is not None:
            arrays["intensity"] = frame.intensity
        if frame.rgb is not None:
            arrays["rgb"] = frame.rgb
        if frame.normals is not None:
            arrays["normals"] = frame.normals
        if frame.curvature is not None:
            arrays["curvature"] = frame.curvature
        if frame.classes is not None:
            arrays["labels"] = frame.classes
        if frame.instances is not None:
            arrays["instances"] = frame.instances
        np.savez_compressed(p, **arrays)

    elif ext in ("bin", "kitti"):
        inte = frame.intensity if frame.intensity is not None else np.zeros(len(frame), dtype=np.float32)
        xyzi = np.hstack([frame.xyz.astype(np.float32), inte.astype(np.float32)[:, None]])
        xyzi.astype("<f4").tofile(p)

    elif ext == "ply":
        write_ply(p, frame.xyz, intensity=frame.intensity, rgb=frame.rgb, normals=frame.normals)

    elif ext == "pcd":
        write_pcd(p, frame.xyz, intensity=frame.intensity, normals=frame.normals)

    else:
        raise ValueError(f"Unsupported output format: '{ext}'")


# ==============================================================================
# PLY Parser & Serializer (ASCII + Binary Little-Endian)
# ==============================================================================

def read_ply(path: Union[str, Path]) -> Tuple[np.ndarray, Optional[np.ndarray], Optional[np.ndarray], Optional[np.ndarray]]:
    """Native pure-Python parser for Stanford PLY files (ASCII & Binary Little Endian)."""
    p = Path(path)
    with open(p, "rb") as f:
        header_lines = []
        while True:
            line = f.readline().decode("latin1").strip()
            header_lines.append(line)
            if line == "end_header":
                break

        is_binary = "format binary_little_endian 1.0" in header_lines
        is_ascii = "format ascii 1.0" in header_lines
        if not (is_binary or is_ascii):
            raise ValueError("PLY format must be ascii 1.0 or binary_little_endian 1.0")

        num_vertices = 0
        properties = []
        for line in header_lines:
            tokens = line.split()
            if len(tokens) >= 3 and tokens[0] == "element" and tokens[1] == "vertex":
                num_vertices = int(tokens[2])
            elif len(tokens) >= 3 and tokens[0] == "property":
                properties.append((tokens[1], tokens[2]))  # (type, name)

        prop_names = [name for _, name in properties]
        if "x" not in prop_names or "y" not in prop_names or "z" not in prop_names:
            raise ValueError("PLY missing required vertex properties x, y, z")

        if is_ascii:
            data = np.loadtxt(f, max_rows=num_vertices)
            if data.ndim == 1 and num_vertices == 1:
                data = data.reshape(1, -1)
            x_idx, y_idx, z_idx = prop_names.index("x"), prop_names.index("y"), prop_names.index("z")
            xyz = data[:, [x_idx, y_idx, z_idx]]
            intensity = data[:, prop_names.index("intensity")] if "intensity" in prop_names else None
            rgb = None
            if "red" in prop_names and "green" in prop_names and "blue" in prop_names:
                r_idx, g_idx, b_idx = prop_names.index("red"), prop_names.index("green"), prop_names.index("blue")
                rgb = data[:, [r_idx, g_idx, b_idx]].astype(np.uint8)
            normals = None
            if "nx" in prop_names and "ny" in prop_names and "nz" in prop_names:
                nx_idx, ny_idx, nz_idx = prop_names.index("nx"), prop_names.index("ny"), prop_names.index("nz")
                normals = data[:, [nx_idx, ny_idx, nz_idx]]
            return xyz, intensity, rgb, normals

        # Binary little-endian
        type_map = {
            "char": "i1", "uchar": "u1", "uint8": "u1", "int8": "i1",
            "short": "i2", "ushort": "u2", "int16": "i2", "uint16": "u2",
            "int": "i4", "uint": "u4", "int32": "i4", "uint32": "u4",
            "float": "f4", "float32": "f4", "double": "f8", "float64": "f8"
        }
        dtype_list = [(name, f"<{type_map[typ]}") for typ, name in properties]
        vertex_dtype = np.dtype(dtype_list)
        records = np.fromfile(f, dtype=vertex_dtype, count=num_vertices)

        xyz = np.vstack([records["x"], records["y"], records["z"]]).T.astype(np.float64)
        intensity = records["intensity"].astype(np.float32) if "intensity" in prop_names else None
        rgb = None
        if "red" in prop_names and "green" in prop_names and "blue" in prop_names:
            rgb = np.vstack([records["red"], records["green"], records["blue"]]).T.astype(np.uint8)
        normals = None
        if "nx" in prop_names and "ny" in prop_names and "nz" in prop_names:
            normals = np.vstack([records["nx"], records["ny"], records["nz"]]).T.astype(np.float64)

        return xyz, intensity, rgb, normals


def write_ply(
    path: Union[str, Path],
    xyz: np.ndarray,
    intensity: Optional[np.ndarray] = None,
    rgb: Optional[np.ndarray] = None,
    normals: Optional[np.ndarray] = None,
    binary: bool = True,
) -> None:
    """Exports point cloud to Stanford PLY (Binary Little Endian by default)."""
    p = Path(path)
    n = len(xyz)

    header = [
        "ply",
        "format binary_little_endian 1.0" if binary else "format ascii 1.0",
        f"element vertex {n}",
        "property float x",
        "property float y",
        "property float z",
    ]
    if intensity is not None:
        header.append("property float intensity")
    if normals is not None:
        header.extend(["property float nx", "property float ny", "property float nz"])
    if rgb is not None:
        header.extend(["property uchar red", "property uchar green", "property uchar blue"])
    header.append("end_header\n")

    with open(p, "wb") as f:
        f.write("\n".join(header).encode("latin1"))
        if binary:
            dtypes = [("x", "<f4"), ("y", "<f4"), ("z", "<f4")]
            data_cols = [xyz[:, 0].astype(np.float32), xyz[:, 1].astype(np.float32), xyz[:, 2].astype(np.float32)]
            if intensity is not None:
                dtypes.append(("intensity", "<f4"))
                data_cols.append(intensity.astype(np.float32))
            if normals is not None:
                dtypes.extend([("nx", "<f4"), ("ny", "<f4"), ("nz", "<f4")])
                data_cols.extend([normals[:, 0].astype(np.float32), normals[:, 1].astype(np.float32), normals[:, 2].astype(np.float32)])
            if rgb is not None:
                dtypes.extend([("red", "u1"), ("green", "u1"), ("blue", "u1")])
                data_cols.extend([rgb[:, 0].astype(np.uint8), rgb[:, 1].astype(np.uint8), rgb[:, 2].astype(np.uint8)])
            
            struct_arr = np.empty(n, dtype=np.dtype(dtypes))
            for (name, _), col in zip(dtypes, data_cols):
                struct_arr[name] = col
            f.write(struct_arr.tobytes())
        else:
            cols = [xyz]
            if intensity is not None:
                cols.append(intensity[:, None])
            if normals is not None:
                cols.append(normals)
            if rgb is not None:
                cols.append(rgb)
            all_data = np.hstack(cols)
            np.savetxt(f, all_data, fmt="%g")


# ==============================================================================
# PCD Parser & Serializer (ASCII + Binary Little-Endian)
# ==============================================================================

def read_pcd(path: Union[str, Path]) -> Tuple[np.ndarray, Optional[np.ndarray], Optional[np.ndarray], Optional[np.ndarray]]:
    """Native pure-Python parser for Point Cloud Library PCD files."""
    p = Path(path)
    with open(p, "rb") as f:
        header = {}
        while True:
            line = f.readline().decode("latin1").strip()
            if not line or line.startswith("#"):
                continue
            tokens = line.split()
            key = tokens[0].upper()
            header[key] = tokens[1:]
            if key == "DATA":
                break

        fields = [f.lower() for f in header["FIELDS"]]
        sizes = [int(s) for s in header["SIZE"]]
        types = header["TYPE"]
        counts = [int(c) for c in header.get("COUNT", [1] * len(fields))]
        points = int(header["POINTS"][0])
        data_mode = header["DATA"][0].lower()

        type_map = {("F", 4): "<f4", ("F", 8): "<f8", ("U", 1): "u1", ("U", 2): "<u2", ("U", 4): "<u4", ("I", 1): "i1", ("I", 2): "<i2", ("I", 4): "<i4"}

        dtype_fields = []
        for name, typ, size, cnt in zip(fields, types, sizes, counts):
            dt = type_map.get((typ.upper(), size), "<f4")
            if cnt > 1:
                dtype_fields.append((name, dt, (cnt,)))
            else:
                dtype_fields.append((name, dt))

        record_dtype = np.dtype(dtype_fields)

        if data_mode == "ascii":
            data = np.loadtxt(f, max_rows=points)
            if data.ndim == 1 and points == 1:
                data = data.reshape(1, -1)
            x_i, y_i, z_i = fields.index("x"), fields.index("y"), fields.index("z")
            xyz = data[:, [x_i, y_i, z_i]].astype(np.float64)
            intensity = data[:, fields.index("intensity")].astype(np.float32) if "intensity" in fields else None
            normals = data[:, [fields.index("normal_x"), fields.index("normal_y"), fields.index("normal_z")]].astype(np.float64) if "normal_x" in fields else None
            return xyz, intensity, None, normals

        elif data_mode == "binary":
            records = np.fromfile(f, dtype=record_dtype, count=points)
            xyz = np.vstack([records["x"], records["y"], records["z"]]).T.astype(np.float64)
            intensity = records["intensity"].astype(np.float32) if "intensity" in fields else None
            normals = np.vstack([records["normal_x"], records["normal_y"], records["normal_z"]]).T.astype(np.float64) if "normal_x" in fields else None
            return xyz, intensity, None, normals
        else:
            raise ValueError(f"Unsupported PCD DATA mode: '{data_mode}'")


def write_pcd(
    path: Union[str, Path],
    xyz: np.ndarray,
    intensity: Optional[np.ndarray] = None,
    normals: Optional[np.ndarray] = None,
    binary: bool = True,
) -> None:
    """Exports point cloud to PCD format."""
    p = Path(path)
    n = len(xyz)
    fields = ["x", "y", "z"]
    sizes = [4, 4, 4]
    types = ["F", "F", "F"]
    counts = [1, 1, 1]

    if intensity is not None:
        fields.append("intensity")
        sizes.append(4)
        types.append("F")
        counts.append(1)

    if normals is not None:
        fields.extend(["normal_x", "normal_y", "normal_z"])
        sizes.extend([4, 4, 4])
        types.extend(["F", "F", "F"])
        counts.extend([1, 1, 1])

    hdr = [
        "# .PCD v0.7 - Point Cloud Data file format",
        "VERSION 0.7",
        f"FIELDS {' '.join(fields)}",
        f"SIZE {' '.join(map(str, sizes))}",
        f"TYPE {' '.join(types)}",
        f"COUNT {' '.join(map(str, counts))}",
        f"WIDTH {n}",
        "HEIGHT 1",
        "VIEWPOINT 0 0 0 1 0 0 0",
        f"POINTS {n}",
        f"DATA {'binary' if binary else 'ascii'}\n",
    ]

    with open(p, "wb") as f:
        f.write("\n".join(hdr).encode("latin1"))
        if binary:
            dtypes = [(name, "<f4") for name in fields]
            struct_arr = np.empty(n, dtype=np.dtype(dtypes))
            struct_arr["x"] = xyz[:, 0].astype(np.float32)
            struct_arr["y"] = xyz[:, 1].astype(np.float32)
            struct_arr["z"] = xyz[:, 2].astype(np.float32)
            if intensity is not None:
                struct_arr["intensity"] = intensity.astype(np.float32)
            if normals is not None:
                struct_arr["normal_x"] = normals[:, 0].astype(np.float32)
                struct_arr["normal_y"] = normals[:, 1].astype(np.float32)
                struct_arr["normal_z"] = normals[:, 2].astype(np.float32)
            f.write(struct_arr.tobytes())
        else:
            cols = [xyz]
            if intensity is not None:
                cols.append(intensity[:, None])
            if normals is not None:
                cols.append(normals)
            np.savetxt(f, np.hstack(cols), fmt="%g")


# ==============================================================================
# LAS Reader (ASPRS LAS 1.2-1.4 Native Unpacker)
# ==============================================================================

def read_las(path: Union[str, Path]) -> Tuple[np.ndarray, Optional[np.ndarray], Optional[np.ndarray], Optional[np.ndarray]]:
    """Native ASPRS LAS format reader (parses headers, scale factors, offsets, and points)."""
    p = Path(path)
    with open(p, "rb") as f:
        sig = f.read(4)
        if sig != b"LASF":
            raise ValueError("Not a valid LAS file (missing LASF signature)")
        
        f.seek(94)
        header_size = struct.unpack("<H", f.read(2))[0]
        offset_to_point_data = struct.unpack("<I", f.read(4))[0]
        
        f.seek(104)
        point_data_format = struct.unpack("<B", f.read(1))[0]
        point_data_record_length = struct.unpack("<H", f.read(2))[0]
        num_point_records = struct.unpack("<I", f.read(4))[0]

        f.seek(131)
        x_scale, y_scale, z_scale = struct.unpack("<ddd", f.read(24))
        x_offset, y_offset, z_offset = struct.unpack("<ddd", f.read(24))

        f.seek(offset_to_point_data)
        raw_bytes = f.read(num_point_records * point_data_record_length)

    # Point formats 0, 1, 2, 3 have XYZ (3x int32) and intensity (uint16)
    dt = np.dtype([
        ("x", "<i4"),
        ("y", "<i4"),
        ("z", "<i4"),
        ("intensity", "<u2"),
        ("flags", "u1"),
        ("classification", "u1"),
    ])

    # Unpack with stride matching record length
    records = np.frombuffer(raw_bytes, dtype=dt, count=num_point_records)
    x = records["x"] * x_scale + x_offset
    y = records["y"] * y_scale + y_offset
    z = records["z"] * z_scale + z_offset
    xyz = np.vstack([x, y, z]).T.astype(np.float64)
    intensity = records["intensity"].astype(np.float32)
    classes = records["classification"].astype(np.int32)

    return xyz, intensity, None, classes


# ==============================================================================
# ROS 2 sensor_msgs/PointCloud2 Serialization & Parsing
# ==============================================================================

def parse_ros2_pointcloud2_dict(msg: dict) -> SpatialFrame:
    """Parses a ROS 2 sensor_msgs/PointCloud2 Python message dictionary."""
    fields = {f["name"]: f for f in msg["fields"]}
    point_step = msg["point_step"]
    width = msg["width"]
    height = msg.get("height", 1)
    n_points = width * height
    raw_data = msg["data"]
    if isinstance(raw_data, (bytes, bytearray)):
        buf = bytes(raw_data)
    else:
        buf = bytes(raw_data)

    dt_map = {1: "i1", 2: "u1", 3: "i2", 4: "u2", 5: "i4", 6: "u4", 7: "<f4", 8: "<f8"}
    
    # Extract x, y, z
    x_off = fields["x"]["offset"]
    y_off = fields["y"]["offset"]
    z_off = fields["z"]["offset"]

    xyz = np.empty((n_points, 3), dtype=np.float64)
    for i in range(n_points):
        base = i * point_step
        x = struct.unpack_from("<f", buf, base + x_off)[0]
        y = struct.unpack_from("<f", buf, base + y_off)[0]
        z = struct.unpack_from("<f", buf, base + z_off)[0]
        xyz[i] = [x, y, z]

    intensity = None
    if "intensity" in fields:
        i_off = fields["intensity"]["offset"]
        inte = np.empty(n_points, dtype=np.float32)
        for i in range(n_points):
            inte[i] = struct.unpack_from("<f", buf, i * point_step + i_off)[0]
        intensity = inte

    meta = FrameMetadata(
        coordinate_frame=msg.get("header", {}).get("frame_id", "sensor_lidar"),
        timestamp_ns=int(msg.get("header", {}).get("stamp", {}).get("sec", 0) * 1e9 + msg.get("header", {}).get("stamp", {}).get("nanosec", 0)),
        sensor_type="ros2_pointcloud2",
    )
    return SpatialFrame(xyz=xyz, intensity=intensity, metadata=meta)


def serialize_ros2_pointcloud2_dict(frame: SpatialFrame) -> dict:
    """Serializes a SpatialFrame into a ROS 2 sensor_msgs/PointCloud2 dictionary structure."""
    n = len(frame)
    point_step = 16  # 3x float32 xyz (12 bytes) + 1x float32 intensity (4 bytes)
    buf = bytearray(n * point_step)

    xyz_f = frame.xyz.astype(np.float32)
    inte_f = frame.intensity.astype(np.float32) if frame.intensity is not None else np.zeros(n, dtype=np.float32)

    for i in range(n):
        struct.pack_into("<ffff", buf, i * point_step, xyz_f[i, 0], xyz_f[i, 1], xyz_f[i, 2], inte_f[i])

    return {
        "header": {
            "frame_id": frame.metadata.coordinate_frame,
            "stamp": {"sec": frame.metadata.timestamp_ns // 1_000_000_000, "nanosec": frame.metadata.timestamp_ns % 1_000_000_000},
        },
        "height": 1,
        "width": n,
        "fields": [
            {"name": "x", "offset": 0, "datatype": 7, "count": 1},
            {"name": "y", "offset": 4, "datatype": 7, "count": 1},
            {"name": "z", "offset": 8, "datatype": 7, "count": 1},
            {"name": "intensity", "offset": 12, "datatype": 7, "count": 1},
        ],
        "is_bigendian": False,
        "point_step": point_step,
        "row_step": n * point_step,
        "data": bytes(buf),
        "is_dense": True,
    }


# ==============================================================================
# Trajectory I/O (KITTI & TUM)
# ==============================================================================

def load_poses(path: Union[str, Path], fmt: str = "kitti") -> np.ndarray:
    """Loads trajectory poses as an (N, 4, 4) array of SE(3) transformation matrices."""
    p = Path(path)
    a = np.loadtxt(p, comments="#", ndmin=2)
    n = len(a)
    T = np.repeat(np.eye(4)[None], n, axis=0)

    if fmt == "kitti":
        if a.shape[1] != 12:
            raise ValueError(f"KITTI pose file must have 12 columns per row, got {a.shape[1]}")
        T[:, :3, :] = a.reshape(-1, 3, 4)
        return T

    elif fmt == "tum":
        # TUM: timestamp tx ty tz qx qy qz qw
        if a.shape[1] != 8:
            raise ValueError(f"TUM trajectory file must have 8 columns per row, got {a.shape[1]}")
        T[:, :3, 3] = a[:, 1:4]
        T[:, :3, :3] = Rotation.from_quat(a[:, 4:8]).as_matrix()
        return T

    else:
        raise ValueError(f"Unsupported trajectory format: '{fmt}' (use 'kitti' or 'tum')")


def save_poses(poses: np.ndarray, path: Union[str, Path], fmt: str = "kitti", timestamps: Optional[np.ndarray] = None) -> None:
    """Saves trajectory poses (N, 4, 4) to KITTI or TUM format."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if poses.ndim != 3 or poses.shape[1:] != (4, 4):
        raise ValueError("Poses must have shape (N, 4, 4)")

    if fmt == "kitti":
        flat = poses[:, :3, :].reshape(len(poses), 12)
        np.savetxt(p, flat, fmt="%.8e")

    elif fmt == "tum":
        ts = timestamps if timestamps is not None else np.arange(len(poses), dtype=np.float64) * 0.1
        trans = poses[:, :3, 3]
        quats = Rotation.from_matrix(poses[:, :3, :3]).as_quat()  # (qx, qy, qz, qw)
        tum_data = np.column_stack([ts, trans, quats])
        np.savetxt(p, tum_data, fmt="%.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f", header="timestamp tx ty tz qx qy qz qw", comments="# ")

    else:
        raise ValueError(f"Unsupported trajectory format: '{fmt}'")


# ==============================================================================
# Velodyne KITTI LiDAR Loader
# ==============================================================================

def read_kitti_velodyne(path: Union[str, Path]) -> Tuple[np.ndarray, np.ndarray]:
    """Reads a KITTI Velodyne HDL-64E LiDAR binary file (.bin).
    
    Data layout: Little-endian float32 quadruples [x, y, z, reflectance].
    Returns (xyz: (N, 3) float64 in meters, intensity: (N,) float32 [0.0, 1.0]).
    """
    p = Path(path)
    raw = np.fromfile(p, dtype="<f4")
    if raw.size % 4 != 0:
        raise ValueError(f"KITTI Velodyne file expects float32 quadruples (XYZI), got total float count {raw.size}")
    reshaped = raw.reshape(-1, 4)
    xyz = reshaped[:, :3].astype(np.float64)
    intensity = reshaped[:, 3].astype(np.float32)
    return xyz, intensity


# ==============================================================================
# Waymo Open Dataset Ingestion (Zero-TensorFlow Pure Protobuf Reader)
# ==============================================================================

def iter_waymo_frames(path: Union[str, Path]):
    """Generator that yields parsed Waymo Frame protobuf messages from a TFRecord or raw frames file."""
    import zlib
    import sys
    try:
        import types
        if "google.protobuf.runtime_version" not in sys.modules:
            dummy_rv = types.ModuleType("google.protobuf.runtime_version")
            dummy_rv.Domain = types.SimpleNamespace(PUBLIC=1)
            dummy_rv.ValidateProtobufRuntimeVersion = lambda *a, **kw: None
            sys.modules["google.protobuf.runtime_version"] = dummy_rv
            import google.protobuf
            setattr(google.protobuf, "runtime_version", dummy_rv)
        else:
            import google.protobuf.runtime_version
            google.protobuf.runtime_version.ValidateProtobufRuntimeVersion = lambda *a, **kw: None
    except Exception:
        pass

    # Ensure Waymo proto package path is searchable
    for search_dir in ["/Users/favl/Downloads", "/Users/favl/Downloads/waymo_open_dataset"]:
        if search_dir not in sys.path:
            sys.path.insert(0, search_dir)

    try:
        from waymo_open_dataset import dataset_pb2, label_pb2
    except ImportError as e:
        raise RuntimeError("Waymo protobuf definitions not found. Ensure waymo_open_dataset is compiled.") from e

    p = Path(path)
    with open(p, "rb") as f:
        while True:
            header = f.read(12)
            if not header or len(header) < 12:
                break
            length = struct.unpack("<Q", header[:8])[0]
            data = f.read(length)
            f.read(4)  # 4 bytes CRC
            if len(data) < length:
                break
            frame = dataset_pb2.Frame()
            frame.ParseFromString(data)
            yield frame


def load_waymo_frame(
    path: Union[str, Path],
    frame_index: int = 0,
    lasers_to_include: Optional[list] = None,
    coordinate_frame: str = "vehicle",
) -> SpatialFrame:
    """Parses a Waymo Open Dataset frame into a canonical SpatialFrame with 3D point cloud & labels.
    
    Extracts:
    - 3D Cartesian coordinates (x, y, z) in meters in the vehicle frame
    - Intensity and elongation channels
    - Ground truth 3D bounding boxes attached as metadata
    """
    import zlib
    from .contracts import BoundingBox3D

    frame = None
    for idx, f in enumerate(iter_waymo_frames(path)):
        if idx == frame_index:
            frame = f
            break

    if frame is None:
        raise ValueError(f"Could not load frame {frame_index} from {path}")

    from waymo_open_dataset import dataset_pb2

    if lasers_to_include is None:
        # Default: TOP laser (64-beam, richest coverage)
        lasers_to_include = [dataset_pb2.LaserName.TOP]

    calib_map = {c.name: c for c in frame.context.laser_calibrations}

    all_xyz = []
    all_intensity = []

    for laser in frame.lasers:
        if laser.name not in lasers_to_include:
            continue
        calib = calib_map.get(laser.name)
        if calib is None:
            continue

        beam_inclinations = np.array(calib.beam_inclinations)
        extrinsic = np.array(calib.extrinsic.transform).reshape(4, 4)

        if not laser.ri_return1.range_image_compressed:
            continue

        decomp = zlib.decompress(laser.ri_return1.range_image_compressed)
        mat = dataset_pb2.MatrixFloat()
        mat.ParseFromString(decomp)
        ri = np.array(mat.data).reshape(mat.shape.dims)  # (H, W, channels)

        H, W, _ = ri.shape
        col_idx = np.arange(W)[None, :]
        azimuth = np.pi - (col_idx + 0.5) / W * (2.0 * np.pi)
        elevation = beam_inclinations[:, None]

        ranges = ri[:, :, 0]
        valid = ranges > 0

        r_v = ranges[valid]
        az_v = np.broadcast_to(azimuth, (H, W))[valid]
        el_v = np.broadcast_to(elevation, (H, W))[valid]
        inte_v = ri[:, :, 1][valid]

        # Convert spherical to sensor cartesian
        x_s = r_v * np.cos(el_v) * np.cos(az_v)
        y_s = r_v * np.cos(el_v) * np.sin(az_v)
        z_s = r_v * np.sin(el_v)

        pts_sensor = np.column_stack([x_s, y_s, z_s, np.ones_like(x_s)])
        # Project to vehicle frame
        pts_vehicle = (pts_sensor @ extrinsic.T)[:, :3]

        all_xyz.append(pts_vehicle)
        all_intensity.append(inte_v)

    if not all_xyz:
        raise ValueError(f"No valid LiDAR points found in frame {frame_index}")

    xyz_fused = np.vstack(all_xyz).astype(np.float64)
    inte_fused = np.concatenate(all_intensity).astype(np.float32)

    # Extract 3D bounding boxes
    boxes = []
    type_name_map = {1: "vehicle", 2: "pedestrian", 3: "sign", 4: "cyclist"}
    for lbl in frame.laser_labels:
        b = lbl.box
        # Rotation around Z axis (heading yaw)
        heading = b.heading
        c, s = np.cos(heading), np.sin(heading)
        R_z = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=np.float64)
        center = np.array([b.center_x, b.center_y, b.center_z], dtype=np.float64)
        extent = np.array([b.length, b.width, b.height], dtype=np.float64)
        box = BoundingBox3D(
            center=center,
            extent=extent,
            rotation=R_z,
            class_id=int(lbl.type),
            label=type_name_map.get(lbl.type, "unknown"),
            confidence=1.0,
        )
        boxes.append(box)

    meta = FrameMetadata(
        coordinate_frame=coordinate_frame,
        timestamp_ns=int(frame.timestamp_micros * 1000),
        sensor_id=f"waymo_{frame.context.name}",
        sensor_type="waymo_lidar_suite",
        extra={
            "context_name": frame.context.name,
            "num_3d_boxes": len(boxes),
            "pose": list(frame.pose.transform) if frame.pose.transform else [],
        },
    )

    return SpatialFrame(
        xyz=xyz_fused,
        intensity=inte_fused,
        metadata=meta,
    )

