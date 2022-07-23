import sys
import os
from pydicom import dcmread
import SimpleITK as sitk
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence
from pydicom.datadict import add_private_dict_entries
from pydicom.datadict import add_private_dict_entry
from pydicom.datadict import DicomDictionary, keyword_dict
from pydicom.dataset import Dataset
from pydicom.datadict import add_private_dict_entries

def reading_dcm_headers_pydicom(dicom_file_path):

    dicom_file = dcmread(dicom_file_path, force = True)
   
    file_path = "E390_without_Transpose_Header_info.txt"
    #sys.stdout = open(file_path, "w")
    print(dicom_file)  
    
    

def reading_dcm_headers_simpleitk(dicom_file_path):
    reader = sitk.ImageFileReader()
    reader.SetFileName(dicom_file_path)
    reader.LoadPrivateTagsOn()
    reader.ReadImageInformation()

    for attributes in reader.GetMetaDataKeys():
        value = reader.GetMetaData(attributes)
        print(f"({attributes}) = = \"{value}\"")

    print(f"Image Size: {reader.GetSize()}")
    print(f"Image PixelType: {sitk.GetPixelIDValueAsString(reader.GetPixelID())}")


reading_dcm_headers_pydicom(r"C:\novartis-imaging-pipeline\medical_imaging_custom_processors\pipeline_components\connectors\Common\IMG_to_DCM_Conversion\E390\DICOM_E390\DICOM\11.dcm")

#reading_dcm_headers_simpleitk(r"COMB157G2301\1000001\sub-COMB157G2301x1000001_ses-EOSx20190507_run-1_T1w\12.dcm")