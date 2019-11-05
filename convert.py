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
    #os.system(command)
    return dst_file


src_dir = 'C:/data/temp'
dst_dir = os.path.join(src_dir,'modified')
os.makedirs(dst_dir, exist_ok=True)
p = re.compile('PNG')

#crop_string = '1589x937+6+104'
crop_string = '666x438+261+602'   # nohrsc
#crop_string = '651x471+258+102' #ndfd
#crop_string = '631x936+926+107' #nbm
montage_files = []

os.chdir(src_dir)
for src_file in glob.glob('*PNG'):
    m = p.search(src_file)
    if m is not None:
        #print(src_file)
        #src = open(srcFile, "r")
        src_file_path = os.path.join(src_dir,str(src_file))
        cropStr = crop_string 
        dst_file = myCrop(crop_string, src_file, dst_dir,'_nohrsc.PNG')


os.chdir(dst_dir)
for card in ('f24*','f36*','f48*','f60*'):
    string = ' ' 
    for mf in glob.glob(card):
        #montage_files.append(os.path.join(dst_dir,mf))
        print(os.path.join(dst_dir,mf))
        string = string + ' ' + os.path.join(dst_dir,mf)
    montage_file = 'montage_' + card[:-1] + '.png'

    cmd = 'montage' + string  + ' -geometry 300x300 ' +  os.path.join(dst_dir,montage_file)
    os.system(cmd)
    print(cmd)
    print('\n\n')

montage_sorted = sorted(montage_files)
print(montage_sorted)