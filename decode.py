import steg_lib as sl
import matplotlib.pyplot as plt 
import numpy as np 
import os
import io
from PIL import Image

file_directory = 'C:\\Users\\baraa\\OneDrive\\Desktop\\StegPhoto\\'
substring = '.tiff'

def read_message(c_image, start_loc, message_length):
    global decoded_message, coded_image_segment
    #coded_image = plt.imread(file_directory + 'coded_image.tiff')
    start_loc_int = int(start_loc)
    message_length_int = int(message_length)
    c_image_array = np.array(c_image)
    c_image_array = c_image_array[:,:,:3]
    coded_image_segment = sl.get_coded_image_segment(c_image_array,start_loc_int,message_length_int)
    binary_message = sl.extract_binary_message(coded_image_segment)
    decoded_message = sl.convert_back(binary_message)
    f = open(file_directory + 'decoded_message','w')
    f.write(decoded_message)
    f.close()