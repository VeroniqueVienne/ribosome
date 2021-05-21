import imageio as io
import numpy as np


def load_tif_image(file_name: str) -> np.ndarray:
    """file_name in .tif format."""
    # open video as array
    video = io.volread(file_name)
    return video.astype(float)
