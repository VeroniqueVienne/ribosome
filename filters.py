"""
This function takes an array and makes the convolution with an horizontal
low pass filter [H2, H1, H0, H1, H2]
"""

import numpy as np
from wavelet_denoizing import Wavelet
from image_processing_utils import make_uniform, remove_trend




def process_imageBTWT(input_video, blur_size: int, tophat_size: int):
    """ We are using this combination of filters for our movie: make_uniform, remove trend, wavelet denoizing, remove trend again.
    We this combination we are able to see the all the particles of a specific size (chosen by the parameters blur_size and
    tophat_size) at the edges of the movie and the center . """
    n_frames = input_video.shape[0]
    n_rows = input_video.shape[1]
    n_columns = input_video.shape[2]
    processed_video = np.zeros(shape=(n_frames, n_rows, n_columns))

    for j in range(n_frames):
        imB = make_uniform(input_video[j], blur_size)
        imBT = remove_trend(imB, tophat_size)
        imBTW = Wavelet(imBT)
        imBTWT = remove_trend(imBTW, tophat_size)
        processed_video[j] = imBTWT

    return processed_video

def process_imageT(input_video, blur_size: int, tophat_size: int):
    """ We can use only the remove trend filter if the illumination of the bruit movie is already uniform"""
    n_frames = input_video.shape[0]
    n_rows = input_video.shape[1]
    n_columns = input_video.shape[2]
    processed_video = np.zeros(shape=(n_frames, n_rows, n_columns))

    for j in range(n_frames):
        imT = remove_trend(input_video, tophat_size)
        
        processed_video[j] = imBTWT

    return processed_video
