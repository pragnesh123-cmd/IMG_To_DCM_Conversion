# Img to Dicom Conversion

## Introduction

Img to DICOM Conversion code is used to convert the .img files into series of DICOM slices.

In the same code, first we are generating the metadata json from proprietary DICOM images and then mapping the JSON metadata information into the headers of converted DICOM files. 


## Description

**In the directory we have following files which are related to conversion :**

**1. img_to_dcm_convrsion.py**\
This is main file which contains the conversion script. 

**2. standard_tag_mapper.csv**\
This csv contains all the standard attributes which is a part of DICOM standard dictionary. This file will use to map the standard DICOM metadata

**3. custom_tag_mapper.py**\
This file contains all the custom and private tags which is not part of DICOM standard dictionary. This file will be used for mapping the custom & private metadata.

**4. img_input.py**\
This file contains input parameters that will be given to conversion.py script.

**5. input.ini**\
This file contain input arguments which are read by img_input.py.


**6. test_conversion.py**\
This file contains test cases.

**7. requirements.txt**\
This file contains list of libraries used in conversion script

**8. license.txt**\
This file contains licensing information for each library.

**The following files are part of source code documentation :**\
i) conf.py\
ii) index.rst\
iii) make.bat\
iv) Makefile\
v) _build dir\
vi) _static dir\
vii) _templates dir

The source code documentation is located at : 

**_build/html/index.html**

## Prerequisites
Ensure following tools available on Windows :
```
Python version 3 or above

The folder which contains the Proprietory DICOMs and .img must be present in root directory.

```

## Configuration

User must give the name of the folder in which the Proprietory DICOMs and .img file are present as input to **input.ini** file.

For example: \
**input.ini**\
[INPUT]\
img_folder = <name_of_the_folder>


## Installation
For Windows:
```
pip install -r requirements.txt

```

## Execution
1. To run conversion 
```
py img_to_dicom_conversion.py
```

2. To run Unit tests
```
python -m unittest test_conversion.py
```

3. To generate test coverage report
```
coverage run -m unittest test_conversion.py
```

4. To view coverage report
```
coverage report
```

## Output

Once we run this file, conversion will take place.

Output will be :

**1."DICOM_name_of_the_folder"**

A new folder **"DICOM_name_of_the_folder"** will be created inside the input folder. This folder will include all the slices of converted DICOM images.

**2. name_of_the_folder.json**

This metadata json file be created inside the input folder. This json contains all the metadata header information that we fetched from proprietary DICOMs and it is mapped in the headers of converted DICOM files.

## Note

All the error will be logged in "error_logs.log" file.# IMG_To_DCM_Conversion
