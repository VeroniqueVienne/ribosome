import numpy as np
import cv2


def make_uniform(image: np.ndarray, blur_size: int = 13):
    """for each pixel of the image, it computes the average level on an area by blur_size*blur_size pixels around this pixel
    and divide by it. This filter permits to uniformize the illumination.
    The choice of the blur_size  should be an odd interger superior to the size of the particle we observe ( 3 pixels in our case)
    and really inferior to the size of an image 512*512 pixels. So we have chosen 13 pixels."""

    blur_kernel = np.ones((blur_size, blur_size), np.float32) / (blur_size ** 2)
    blur_avg = cv2.filter2D(image, -1, blur_kernel)
    normalized_image = image / blur_avg

    return normalized_image


def remove_trend(image, tophat_size=9):
    """Remove the background trend from the image.
    The choice of the tophat_size in pixels corresponds to the square of the size of our particle (3 pixels)."""
    tophat_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (tophat_size, tophat_size)
    )
    tophat_image = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, tophat_kernel)
    return tophat_image
