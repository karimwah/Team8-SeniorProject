import steg_lib as sl
import matplotlib.pyplot as plt 
import numpy as np 
import os
import io
from PIL import Image

file_directory = 'C:\\Users\\baraa\\OneDrive\\Desktop\\StegPhoto\\'
substring = '.tiff'
global pic_array, im, start_integer



# generate file list from file_directory (with exception handling)
'''
file_list = []
try:
    all_files = os.listdir(file_directory)
except:
    print('something wrong with your directory')
for i in range(0,len(all_files)):
    if substring in all_files[i]:
        file_list.append(all_files[i])
if len(file_list) == 0:
    print('no files with this specification')
    print('place .tiff image file(s) in directory and try again')
file_list.sort() # needed to correct os.listdir() order
'''

#im = Image.open(file_directory + file_select.value) # this needs to assign the image to this variable 'im'
#pic_array = np.array(im)[:,:,:3] #drop the alpha channel, if present; I think this is creating an array from the image


## This is to encode the message in the image
## This includes all 5 functions it takes to encode the message and drop it into the folder
def insert_message(image, message, start_loc):
    global str_message_length
    (binary_message, str_message_length) = sl.convert(message)
    (image_vector, carrier_segment, length_of_binary, 
        rows, cols, colors) = sl.prepare_carrier_segment(image, 
        binary_message, start_loc)
    coded_image_segment = sl.insert_message(carrier_segment, 
        binary_message, length_of_binary)
    coded_image_vector = sl.insert_coded_segment(image_vector,
        coded_image_segment,start_loc)
    coded_image = sl.get_coded_image(coded_image_vector,rows,cols,colors)
    # save new image with message, provide message length
    plt.imsave(file_directory + 'coded_image.tiff',coded_image, format = 'tiff')
    s = str(str_message_length)
    output_text = 'Message string length is: ' + s \
        + '\n and message start location is: ' + str(start_loc)
    f = open(file_directory + 'message_info','w')
    f.write(output_text)
    f.close()

