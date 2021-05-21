import numpy as np
import trackpy as tp
import pandas as pd


def link_particles(
    video: np.ndarray,
    particle_diameter: int = 5,
    min_mass=0.1,
    pixel_range=3,
    n_memory_frames: int = 0,
)-> (pd.DataFrame, pd.DataFrame):
    """Link particules.

    Args:
        video ([type]): the preprocessed video with the different filter BTWT
        
        particle_diameter (int, odd): maximum diameter of spot to be located, in pixels. . 
        Our particle are about 3 pixels in our camera so we chose the odd 5 just above for this parameter. 
        For an other type of particle, the operateur should determine the size of his particle using the diffraction limit and depending the size 
        of the size of the pixels of the camera used: he would be able to determine the size of his particle in pixel. The value chosen 
        for the particle_diameter should be the integer odd just above the size in pixels of the particle used.
        
        
        min_mass (float, optional): minimum mass (average intensity) of spot. Defaults to 0.1.
        To chose the parameter  min_mass the operateur should take one frame of the preprocessed movie with the filters (BTWT)
        and see the level of gray in an area of blur_size* blur_size ( 13*13 pixels in our case) centered in a particle and 
        an other area of the same size where there is only the background. We have to make the difference of the levels of gray
        to have the range of the min_mass: the min_mass will correspon to a value between 0 to the diffrence of the gray level.
        If the value chosen by the operateur is close to the max diffrence level of gray , then that mean we are oly looking 
        at the particles which are really shiny. On the other case, when it is close to 0 then we are also detecting a lot of noise.
        So the operateur shoould chose this value according to what he really wants to observe.
        
        pixel_range (int, optional): search range (maximum displacement between frames) around spot, in pixels. Defaults to half of 
        the particle_diameter if the particles are immobile. Here we have 3 pixels for our system.
        
        n_memory_frames (int, optional): memory (maximum frames a particle can disappear, reappear and be considered the same particle), in frames.
        Defaults to 0. We have chosen 0 because we don't want particular which blink.'
    """
    
    
    # particle detection using trackpy. 
    """This function of trackpy permits to detect the particles of a certain particle_diameter and which mass is abose the min_mass in all 
    frames of the video"""

    located_particles = tp.batch(
        video, diameter=particle_diameter, minmass=min_mass, percentile=60
    )
    
    
    # particle linking using trackpy
    """This function of trackpy takes in input the dataframe located_particles given by trackpy.batch and by using the criteria of the 
    pixel_range and the n_memory_frames: it will accord a trajectory for  each particle and a label"""
    linked_particles = tp.link_df(
        located_particles, pixel_range, memory=n_memory_frames
    )

    return linked_particles
