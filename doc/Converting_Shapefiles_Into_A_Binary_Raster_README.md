# Converting_Shapefiles_Into_A_Binary_Raster Notebook

This notebook helps us in achieving the followings:

* It generates the tif files by rasterising the manually annotated shapefiles.
* It will first considers the non-water bodies annotations and generates the tif files by having the difference from its corresponding water bodies annotations.
* It will then considers the remaining ones, the left water bodies annotation which do not contain any not water bodies within the shapefiles.