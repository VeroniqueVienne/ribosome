import imageio as io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ruptures as rpt
import os.path
from random import *


from load import load_tif_image
from separate_images import image_separation
from filters import process_imageBTWT, process_imageT
from link_particules import link_particles
from tracking import optical_flow_intensity
from colocalization_of_red_green_single_particle import colocalization
from detection_of_breaks_in_trace import breaks_in_trace




#%% Choose one file

FILENAME = "A5SL_0511_6TpR.tif"


#%%# load data
video=load_tif_image(FILENAME)

# separate image to obtain the red_movie and the green_movie
red_video, green_video = image_separation(video)
L = []

L.append(red_video)
L.append(green_video)

n_frames, n_raws, n_columns = L[0].shape  #the shape of the red_video / green_video

#%% Preprocessing :image treatment

# constants for the preprocessing
'''those parameters below must be chosen wisely acording to the size of the image.shape of the movie and the size of the particle . Go and check
image_processing_utils.py to know how we chose theses parameters'''
blur_size = 13
tophat_size = 9

'''the combination of treatment for video preposcessing  will also depends on the quality of the illumination of the movie. For our movie,
 the illumination is a gaussian profile so the particles in the center are more excited compared to the ones at the edges. Since the signal
to noise ratio is really low so we use this particular combination of filters which works on our movie.
'''
video_preprocessed_red = process_imageBTWT(L[0], blur_size, tophat_size)  # red_movie treated with the filters
video_preprocessed_green = process_imageBTWT(L[1], blur_size, tophat_size) # green_movie treated with the filters

#%% detection and tracking the particles

particle_diameter= 5
min_mass=0.1
pixel_range=3
n_memory_frames=0

linked_particles_red = link_particles(video_preprocessed_red, particle_diameter, min_mass, pixel_range, n_memory_frames)


linked_particles_green = link_particles(video_preprocessed_green, particle_diameter, min_mass, pixel_range, n_memory_frames)


#%% computing the signal of the intensity for all the particles found at the frame 0 and tracked in the full movie

'''we are only tracking particles present at the frame 0 in the full movie'''

particle_radius=3

followed_particles_red = optical_flow_intensity(
    linked_particles_red, video_preprocessed_red, particle_radius
)

followed_particles_green = optical_flow_intensity(
    linked_particles_green, video_preprocessed_green, particle_radius
)

#%% colocalization
''' percentage of the colocalization of the red and green particles of the frame 0: 
    it is an indicator of the quality of the hybridization'''

single_particle_red=followed_particles_red[followed_particles_red.frame==0]

single_particle_green=followed_particles_green[followed_particles_green.frame==0]



colocalization(single_particle_red,single_particle_green , 3)


#%% detection of breakpoints

'''the threshold for rupture that the operateur has to choose ?'''

THRESHOLD=0.1 

filename_red= FILENAME.split('.')[0] + '_red'
filename_green= FILENAME.split('.')[0]+ '_green'

os.mkdir(filename_red+'/')
os.mkdir(filename_red+'/keep0/')
os.mkdir(filename_red+'/keep1/')

os.mkdir(filename_green+'/')
os.mkdir(filename_green+'/keep0/')
os.mkdir(filename_green+'/keep1/')

#%% detection of breakpoints

df_breaks_red=breaks_in_trace(filename_red,followed_particles_red,video_preprocessed_red,THRESHOLD )

df_breaks_green=breaks_in_trace(filename_green,followed_particles_green,video_preprocessed_green,THRESHOLD )

#%% selection of traces of single particles: partciles which nevers die or particles which have only one break up point

#%% colocalization of red and green single particles





