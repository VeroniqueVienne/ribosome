# ribosomeload.py permits to load the fileseparate_images.py permits to separate the red_video and the green_video


filters.py calls image_processing_utils.py and wavelet_denoizing.py It permits to make all the filtering to remove the background noize and the make the illumination uniform in order to see the signals of all the particles  of a specified size and which mass is above a certain criteria from all the movie 


link_particules.py calls a library called trackpy which permits to detect the particleswith a certain criteria chosen by the operator. And also will accord a trajectory for each particle and a label (cf link_particules.py for more details)


tracking.py permits to compute the signal of the intensityfor all the particles found at the frame 0 that we are tracking in the full movie


colocalization_of_red_green_single_particle.pypermits to calculate the percentage of the colocalization of the red and green particles of the frame 0: it is an indicator of the quality of the hybridization


detection_of_breaks_in_trace.py permits to detect the break up point using the library calledrupture
