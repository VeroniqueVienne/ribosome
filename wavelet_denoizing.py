"""
This function takes an array and makes the convolution with an horizontal
low pass filter [H2, H1, H0, H1, H2]
"""

import imageio as io
import cv2
import numpy as np
import pandas as pd
import trackpy as tp
import skimage
import os, sys
from scipy.signal import find_peaks
from scipy import signal
from time import time
from matplotlib.pyplot import *

import ruptures as rp


# parameters for the filters
H0 = 3.0 / 8
H1 = 1.0 / 4
H2 = 1.0 / 16


def LowPass1():
    LowPass = np.array([H2, H1, H0, H1, H2])
    LowPassV = LowPass.reshape(-1, 1)
    LowPassH = LowPass.reshape(1, -1)
    Array1 = np.dot(LowPassV, LowPassH)
    return Array1


def LowPass2():
    LowPass = np.array([H2, 0, H1, 0, H0, 0, H1, 0, H2])
    LowPassV = LowPass.reshape(-1, 1)
    LowPassH = LowPass.reshape(1, -1)
    Array2 = np.dot(LowPassV, LowPassH)
    return Array2


def Wavelet2(Array, Array1, Array2):
    LC1 = signal.convolve2d(Array, Array1, mode="same")
    LC2 = signal.convolve2d(LC1, Array2, mode="same")
    NewArray = LC1 - LC2
    return NewArray


def Wavelet(image):
    LP1 = LowPass1()
    LP2 = LowPass2()
    NbRows = image.shape[0]
    NbColumns = image.shape[1]

    framesW = np.zeros((NbRows, NbColumns))
    framesW = Wavelet2(image, LP1, LP2)
    return framesW
