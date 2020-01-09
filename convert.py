# -*- coding: utf-8 -*-
"""
This script takes png screen shots of NBM viewer data,
crops the 4 panes, and creates mosaics for each forecast
hour containing the different forecast sources as well as verification 
with data in the following configuration

   top  left : NDFD
   top right : NBMv32
 bottom left : verifiying dataset (URMA, NOHRSC, etc.)
bottom right : NBMv31

NBM viewer settings
                   Type : Event Review
               Location : GRR or MI
    Analysis Hour (UTC) : 12Z works the best
                  Range : Mid 
   NDFD Issuance offset : 06 to reflect the forecast
                          being based on 6 hours earlier guidance

It's easiest to take a screen shot of the entire browser window
and then use Paint or some other application to find the x,y pixel
coordinates for the top left corners of the crop areas associated
with top left and bottom right panes in the screen shot

The filenames of these screen-captured images need to follow this example:
    
    SnowAmt24_20191113-12Z_F72.PNG

      SnowAmt24 : forecast element (easiest to emulate NBM naming
                  convention; in this case, 24 hour snowfall)
       20191113 : verifying date
            12Z : verifying hour
            F72 : hours in future from forecast time

"""

import glob
import os


def myResize(resizeImages, resizeValue, run):
    if run is True:
        resizeCommand = "mogrify -resize " + resizeValue + " " + resizeImages
        os.system(resizeCommand);
        print ("done resizing")
    return

def myCrop(src_path,dst_path,crop_string, run):
    """
    src_file_dir : example - 'C:/data/{case_name}
    example: SnowAmt24_20191113-12Z_F24.PNG
    """  
    command = "convert -crop " + crop_string + " +repage " + src_path + ' ' + dst_path
    if run is True:
        print(command)
        os.system(command)
    
    return

def uniq(my_list):
    """
    Takes a list, sorts it, elimates duplicates, and returns new list
    """
    my_list.sort()
    output = []
    for x in my_list:
        if x not in output:
            output.append(x)
    output.sort()
    return output

src_dir = 'C:/data/20191111/verif/test'
dst_dir = os.path.join(src_dir,'modified')
os.makedirs(dst_dir, exist_ok=True)

"""
Below is for GRR, then zoom out one step.
Also deselect annoying CWA boundary map

upper_left = [511,256]
lower_right = [1239,715]
img_width = 340
img_height = 325
"""

"""
Below is for MI projection, request it be shifted a little farther
south instead of right at IN border.
"""
#top_left = [497,228]        # top left corner of crop area for top left image 

bottom_right = [1227,686]   # top left corner of crop area for bottom right image
img_width = 325
img_height = 388

top_left = [496,207]
bottom_right = [1226,666]



top_left = ['+'+str(a) for a in top_left]
bottom_right = ['+'+str(b) for b in bottom_right]
img_width = 300
img_height = 400

crop_dim = str(img_width) + 'x' + str(img_height)
x = [top_left[0],bottom_right[0]]
y = [top_left[1],bottom_right[1]]

coor_list = [crop_dim+a+b for b in y for a in x]

image = {'ndfd':{'crop':coor_list[0],'extension':'ndfd'},               # upper left
         'nbm32':{'crop':coor_list[1],'extension':'nbm32'},             # upper right
         #'nohrsc':{'crop':coor_list[2],'nohrsc.PNG'},                  
         'observed':{'crop':coor_list[2],'extension':'observed'},       # lower left
         'nbm31':{'crop':coor_list[3],'extension':'nbm31'}              # lower right
}

montage_files = []
fcst_hour_list = []
valid_time_list = []
forecast_element_list = []
os.chdir(src_dir)
for src_file in glob.glob('*PNG'):
    """
    example: SnowAmt24_20191113-12Z_F24.PNG
    """  
    if 'montage' not in src_file:
        src_path = os.path.join(src_dir,str(src_file))
        dst_dir = os.path.join(src_dir,'modified')

  
        fname_split = str(src_file).split('_')

        forecast_element = str(fname_split[0])          # SnowAmt24
        forecast_element_list.append(forecast_element)

        valid_time = str(fname_split[1])         # 20191113-12Z
        valid_time_list.append(valid_time)

        fcst_hour = str(fname_split[2][:-4])     # F24
        fcst_hour_list.append(fcst_hour)

        # here is where each image gets split into four panels, which requires the ordering in the
        # images dictionary
        for key in image:
            data_source = key
            crop_string = image[key]['crop']                

            print(crop_string,data_source)
            dst_file_name =  src_file[:-4] + '_' + data_source + '.PNG'
            dst_path = os.path.join(src_dir,'modified',dst_file_name)
            myCrop(src_path, dst_path, crop_string, False);
            myResize(dst_path,crop_dim,False);


all_fcst_hours = uniq(fcst_hour_list)
all_fcst_hours.reverse()
all_valid_time_strs = uniq(valid_time_list)
all_data_srcs = [a for a in image.keys()]
all_forecast_elements = uniq(forecast_element_list)
valid_timestr = all_valid_time_strs[0]


# create forecast source montage each containing all forecast hours for the forecast element (and verification)
# using a given forecast source
for forecast_element in all_forecast_elements:
    for data_src in all_data_srcs:
        cmd = ' montage '
        montage_fname = 'montage_' + forecast_element + '_' + data_src + '.png'
        montage_fpath = os.path.join(dst_dir,montage_fname)
        montage_title = '"' + forecast_element + ' ' + data_src + '"'
        for fcst_hour in all_fcst_hours:
            new_fname = forecast_element + '_' + valid_timestr + '_' + fcst_hour + '_' + data_src + '.PNG'
            full_path = os.path.join(dst_dir,new_fname)
            label_name = '"' + fcst_hour + '" '
            fcst_string = '-label ' + label_name + ' -pointsize 22 ' + full_path + ' ' 
            cmd = cmd + fcst_string

        verif_filename = forecast_element + '_' + valid_timestr + '_F24_observed.PNG'
        verif_full_path = os.path.join(dst_dir,verif_filename)
        verif_label_name = '"Observed"'
        verif_fcst_string = '-label ' + verif_label_name + ' -pointsize 22 ' + verif_full_path + ' '         
        cmd = cmd + verif_fcst_string 
        cmd = cmd + ' -title ' + montage_title + ' -pointsize 24 -geometry ' + crop_dim + '+10+6 ' + montage_fpath        
        if data_src != 'observed':
            print(cmd)
            print('\n\n')
            os.system(cmd)


# create forecast hour montages each containing the different forecast source for that forecast hour
for forecast_element in all_forecast_elements:
    for fcst_hour in all_fcst_hours:
        cmd = ' montage '
        montage_fname = 'montage_' + forecast_element + '_' + fcst_hour + '.png'
        montage_fpath = os.path.join(dst_dir,montage_fname)
        montage_title = '"Valid ' + valid_timestr + ' ' + fcst_hour + '" ' 
        for data_src in all_data_srcs:
            new_fname = forecast_element + '_' + valid_timestr + '_' + fcst_hour + '_' + data_src + '.PNG'
            full_path = os.path.join(dst_dir,new_fname)
            label_name = '"' + forecast_element + ' ' + data_src + '" '
            cmd = cmd + '-label ' + label_name + ' -pointsize 22 ' + full_path + ' ' 
        cmd = cmd + ' -title ' + montage_title + ' -pointsize 24 -geometry ' + crop_dim + '+10+6 ' + montage_fpath        
        if cmd is not None:
            print(cmd)
            print('\n\n')
            os.system(cmd)

            

#montage_sorted = sorted(montage_files)
#print(montage_sorted)
