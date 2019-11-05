# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 11:47:11 2019

@author: thomas.turnage
"""

import glob
import os
import re


def myCrop(cropStr, src_file, dst_dir, dst_extension):
    out_file = src_file[:-4] + dst_extension
    #print(out_file)
    dst_file = os.path.join(dst_dir,out_file)
    print(dst_file)
    command = "convert -crop " + cropStr + " +repage " + src_file + ' ' + dst_file
    print(command)
    os.system(command)
    return dst_file


src_dir = 'C:/data/NBM-ver/screen'
dst_dir = os.path.join(src_dir,'modified')
os.makedirs(dst_dir, exist_ok=True)
p = re.compile('PNG')

image = {'ndfd':{'crop':'730x435+10+6','extension':'_ndfd.PNG'},
         'nbm_31':{'crop':'666x438+740+6','extension':'_nbm31.PNG'},
         'nbm_32':{'crop':'731x413+735+430','extension':'_nbm32.PNG'},
         'nohrsc':{'crop':'730x369+9+471','extension':'_nohrsc.PNG'}}

#crop_string = '1589x937+6+104'
#crop_string = '666x438+261+602'   # nohrsc
#crop_string = '651x471+258+102' #ndfd
#crop_string = '631x936+926+107' #nbm
montage_files = []

os.chdir(src_dir)
for src_file in glob.glob('*PNG'):
    m = p.search(src_file)
    if 2 > 1:
    #if m is not None:
        #print(src_file)
        #src = open(srcFile, "r")
        src_file_path = os.path.join(src_dir,str(src_file))
        for key in image:
            print(key)
            crop_string = image[key]['crop']
            ext = image[key]['extension']
            print(crop_string,ext)
            dst_file = myCrop(crop_string, src_file, dst_dir, ext)


os.chdir(dst_dir)
for card in ('f24*','f36*','f48*','f60*'):
    string = ' ' 
    for mf in glob.glob(card):
        #montage_files.append(os.path.join(dst_dir,mf))
        geom = ' '
        print(os.path.join(dst_dir,mf))
#        if 'nbm' in mf:
#            geom = ' -geometry 300x300+0+0 '
#        else:
#            geom = ' -geometry 400x400+300-6 '            
        
        string = string + ' ' + os.path.join(dst_dir,mf)
    montage_file = 'montage_' + card[:-1] + '.png'

    cmd = 'montage' + string  + geom +  os.path.join(dst_dir,montage_file)
    os.system(cmd)
    print(cmd)

#montage_sorted = sorted(montage_files)
#print(montage_sorted)
