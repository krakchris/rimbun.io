import os
import numpy as np

def wgs2epsg(x,y):
    # calculates EPSG code from xy coordinate in wgs84 format
    EPSG = int(32700-round((45+y)/90,0)*100+round((183+x)/6,0))
    UTM_EPSG_code = EPSG
    
    return UTM_EPSG_code

def make_dir(dir_path):
    # checks if a directory exists, if not create it.
        try:
            # Create  Directory  MyDirectory 
            os.mkdir(dir_path)
            #print if directory created successfully...
            print("Directory " , dir_path ,  " Created") 
        except FileExistsError:
            ##print if directory already exists...
            print("Directory " , dir_path ,  " already exists...")
            
def reshape(index):
    index = np.reshape(index,[1,index.shape[0],index.shape[1]])
    return(index)