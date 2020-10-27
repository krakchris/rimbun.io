import numpy as np
import requests
import os

def wgs2epsg(x,y):
    # calculates EPSG code from xy coordinate in wgs84 format
    EPSG = int(32700-round((45+y)/90,0)*100+round((183+x)/6,0))
    UTM_EPSG_code = EPSG
    
    return UTM_EPSG_code

def make_dir(dir_path):
    # checks if a directory exists, if not create it.
        try:
            # Create  Directory  MyDirectory 
            os.makedirs(dir_path)
            #print if directory created successfully...
            print("Directory " , dir_path ,  " Created") 
        except FileExistsError:
            ##print if directory already exists...
            print("Directory " , dir_path ,  " already exists...")
            
def reshape(index):
    index = np.reshape(index,[1,index.shape[0],index.shape[1]])
    return(index)

def load(filename, input_shape=None):
    np_image = Image.open(filename)
    np_image = np.array(np_image).astype('float32')/255
    np_image = transform.resize(np_image, input_shape)
    np_image = np.expand_dims(np_image, axis=0)
    return np_image

def download_file(url, local):
    
    local_filename = local
    
    r = requests.get(url, stream=True)
    
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                
    return local_filename

def check_valid_geometries(shapefile_path):
    
    shape_list = []
    
    # check crs
    if fiona.open(shapefile_path).crs['init'] != 'epsg:4326':
        print('crs is not epsg:4326, skipping...')
        
        crs_check = False
    else:
        crs_check = True
        
    data = []

    for pol in fiona.open(shapefile_path):
        if pol['geometry'] != None:
                shape_list.append(pol)
                data.append(pol)
            
    return shape_list, data, crs_check