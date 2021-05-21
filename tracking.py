import numpy as np
import pandas as pd
import trackpy as tp
import skimage
import os, sys
from scipy.signal import find_peaks
from link_particules import link_particles






def compute_intensity(
    image, position_x: float, position_y: float, particule_radius: int
) -> float:
    '''function which permits to clculate the intensity in a position( xp, yp)'''
    neighbourhood_size = (particule_radius - 1) // 2
    position_x_int = int(position_x)
    position_y_int = int(position_y)
    nb_rows, nb_columns = image.shape
    if (
        position_y_int >= neighbourhood_size
        and position_y_int <= nb_rows - neighbourhood_size - 1
        and position_x_int >= neighbourhood_size
        and position_x_int <= nb_columns - neighbourhood_size - 1
    ):
        intensity_value = (
            sum(
                sum(
                    image[
                        position_y_int - neighbourhood_size : position_y_int + neighbourhood_size + 1,
                        position_x_int - neighbourhood_size : position_x_int + neighbourhood_size + 1,
                    ]
                )
            )
            / particule_radius ** 2
        )
    else:
        intensity_value = 1.0
    return intensity_value




def optical_flow(linked_particles, n_frames: int) -> pd.DataFrame:
    '''For each particle found at the frame 0, we create a subdataframe containing
    the same columns as linked_particles with a n_frames number of rows .
     Then we concatene all the subdataframes in order to obtain a dataframe of size
     n_frames*nB of particles (frame0) rows . It a dataframe for initialization because we copy n_frames 
     times the subdataframe dor the nB particles'''
     
    particules_on_first_frame = linked_particles[linked_particles.frame == 0]
    

    for item, row in particules_on_first_frame.iterrows():
        a=item
        particules_on_first_frame.loc[item, "particle"] = a

    particules_on_first_frame.drop(
        ["mass", "size", "raw_mass", "ep", "ecc"], axis=1, inplace=True
    )
    fol_part1 = particules_on_first_frame.copy()
    fol_part2 = particules_on_first_frame.copy()

    for f in range(n_frames):
        if f > 0:
            fol_part2.frame = fol_part1.frame + f
            particules_on_first_frame = pd.concat(
                [particules_on_first_frame, fol_part2], ignore_index=True
            )
    return particules_on_first_frame


def optical_flow_intensity(linked_particles, video, particle_radius) -> pd.DataFrame:
    ''' here we calculate the intensity value and put that on the column signal '''
    n_frames = video.shape[0]
    particules_on_first_frame = optical_flow(linked_particles, n_frames)

    for row in particules_on_first_frame.itertuples():

        intensity_value = compute_intensity(video[row.frame], row.x, row.y, particle_radius)

        particules_on_first_frame.at[row.Index, "signal"] = intensity_value

    return particules_on_first_frame
