import numpy as np


def image_separation(movie: np.ndarray) -> (np.ndarray, np.ndarray):
    """Separate red movie and green movie"""
    red_video = movie[::2]
    green_video= movie[1::2]
    return red_video, green_video
