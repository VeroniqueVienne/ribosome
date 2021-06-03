"""
- Take film
- separate red and green channels

Then on each image seprately:
- preprocess,
- detect and track particles,
- change-point detection
"""
import os
from colocalization_of_red_green_single_particle import colocalization
from detection_of_breaks_in_trace import breaks_in_trace
from filters import process_imageBTWT
from link_particules import link_particles
from load import load_tif_image
from separate_images import image_separation
from tracking import optical_flow_intensity

#%% Choose one file

FILENAME = "A5SL_0511_6TpR.tif"


#%%# load data
video = load_tif_image(FILENAME)

# separate image to obtain the red_movie and the green_movie
red_video, green_video = image_separation(video)
movie_list = [red_video, green_video]
n_frames, n_raws, n_columns = red_video.shape  # the shape of the red_video / green_video

#%% Preprocessing :image treatment

# parameters for the preprocessing
# those parameters below must be chosen wisely acording to the size of the image and the size of the particle.
# Go and check image_processing_utils.py to know how we chose theses parameters
blur_size = 13
tophat_size = 9

# For uniform illumination: blurring, tophat filter, wavelet filter

video_preprocessed_red = process_imageBTWT(
    red_video, blur_size, tophat_size
)  # filtered red movie
video_preprocessed_green = process_imageBTWT(
    green_video, blur_size, tophat_size
)  # filtered green movie

#%% detection and tracking the particles

particle_diameter = 5
min_mass = 0.1
pixel_range = 3
n_memory_frames = 0

linked_particles_red = link_particles(
    video_preprocessed_red,
    particle_diameter,
    min_mass,
    pixel_range,
    n_memory_frames,
)


linked_particles_green = link_particles(
    video_preprocessed_green,
    particle_diameter,
    min_mass,
    pixel_range,
    n_memory_frames,
)


#%% compute intensity for all the particles found at the frame 0 and tracked in the full movie

particle_radius = 3

followed_particles_red = optical_flow_intensity(
    linked_particles_red, video_preprocessed_red, particle_radius
)

followed_particles_green = optical_flow_intensity(
    linked_particles_green, video_preprocessed_green, particle_radius
)

#%% colocalization
""" percentage of the colocalization of the red and green particles of the frame 0: 
    it is an indicator of the quality of the hybridization"""

single_particle_red = followed_particles_red[followed_particles_red.frame == 0]

single_particle_green = followed_particles_green[followed_particles_green.frame == 0]


colocalization(single_particle_red, single_particle_green, 3)


#%% detection of breakpoints

"""the threshold for rupture that the operateur has to choose ?"""

THRESHOLD = 0.1

filename_red = FILENAME.split(".")[0] + "_red"
filename_green = FILENAME.split(".")[0] + "_green"

os.mkdir(filename_red + "/")
os.mkdir(filename_red + "/keep0/")
os.mkdir(filename_red + "/keep1/")

os.mkdir(filename_green + "/")
os.mkdir(filename_green + "/keep0/")
os.mkdir(filename_green + "/keep1/")

#%% detection of breakpoints

df_breaks_red = breaks_in_trace(
    filename_red, followed_particles_red, video_preprocessed_red, THRESHOLD
)

df_breaks_green = breaks_in_trace(
    filename_green,
    followed_particles_green,
    video_preprocessed_green,
    THRESHOLD,
)

#%% selection of traces of single particles: partciles which nevers die or particles which have only one break up point

#%% colocalization of red and green single particles
