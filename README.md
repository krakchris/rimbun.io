# rimbun.io

# Table of contents

- Intro
- Description
- How To Use
- Input
- Output 
- Basemodels
- Open data
- Alternatives

# Introduction

Rimbun.io is an open source tool developed by Green City Watch in collaboration with The World Bank and the Government of Indonesia. The tools are build to leverage remote sensing and machine learning, known as “geoAI” to measure urban blue spaces and riperian zones.

![image](https://github.com/krakchris/rimbun.io/blob/master/img/lake_example.png)

***

# Description

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

Rimbun.io is and open source Water Detection algorithm using U-net model infrastructure. 
Rimbun.io was designed to run on AWS EC2 instances but for improving the model training data needs to be made on local computers using GIS software.

## How to use

The experimental workflow in this repository mainly consists of jupyter notebooks. The easiest way to use these notebooks is to start a AWS Deep learning AMI. The notebooks have been tested on an ubuntu deep learning AMI. Requirement files are supplied in this repository. 

## Input
* 4 or 8 band aerial or satellite imagery with a spatial resolution between 20-80cm including RGBI bands
* Trained model or Water annotations

## Output
* Water Detection Shapefiles and metadata

## Algorithm Steps
### Creating inferences from large satellite/aerial image


1. Collect imagery
    - purpose: downloading imagery from gbdx 
    - input: city name
    - output: gridded imagery data on s3 drive
    
1. Run inference
    - purpose: detecting water bodies on satellite imagery
    - input: satellite data (step 1) and pre-trained model (available on s3)
    - output: vector data of water areas
    
1. Measure extra veriables
    - purpose: measure changes in green cover and overlap with percil map
    - input: vector data of water bodies
    - output: green cover fraction values surrounding water bodies over time, values for percil overlap per type for water body


### (Re)Training a model on hand annotations from Image

* Collect imagery
* Creating trianing data
* Retrain model
* Run inference
* Measure metadata

## Basemodels
We have tested the U-net model architecture to be working.

The base model can be downloaded here: [Link](www.greencitywatch.com)

## OpenData
Treetect is tested on Worldview-2/3 imagery.
If you do not have access to Commercial High Resolution Imagery you can use open datasets provided by [Maxar](https://www.maxar.com/open-data) (covering specific sites only). Or have a look at the NAIP Dataset [here](https://azure.microsoft.com/en-us/services/open-datasets/catalog/naip/) covering the USA (not tested). Otherwise check out [this](https://zhangbin0917.github.io/2018/06/12/%E9%81%A5%E6%84%9F%E6%95%B0%E6%8D%AE%E9%9B%86/) vast collection of remote sensing data.  

## Alternatives
There are several open source frameworks for applying machine learning to satellite imagery. Find a selection below:
- [Rastervision](https://github.com/azavea/raster-vision)
- [EO-learn](https://github.com/sentinel-hub/eo-learn)
- [Robosat](https://github.com/mapbox/robosat)
- [Solaris](https://github.com/cosmiq/solaris)
- [Neat-EO](https://archive.fosdem.org/2020/schedule/event/robosat_pink_deep_learning_computer_vision_patterns_extraction_at_scale/)
