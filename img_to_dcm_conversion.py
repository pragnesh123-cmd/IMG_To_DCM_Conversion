"""
IMG to DICOM Conversion 
---------------------------------------

This is the Python Package that converts the IMG 
file into series of DICOM files. The metadata information which is present in Proprietory DICOM files are fetched into a metadata JSON file and then they are mapped into headers of converted DICOM files.

The libraries used in code: 

1. numpy : Used for reading the img images and handling of the arrays

3. pandas : Used for dataframe handling

4. pydicom : Used for mapping the custom and private metadata

5. SimpleITK : Used for converting the arrays into DICOM images
"""
# Importing libraries
import re
import os
import time
import json
import logging
import numpy as np
import pandas as pd
from os import path
from glob import glob
from pathlib import Path
import SimpleITK as sitk
from tqdm import tqdm
from pydicom import dcmread
from img_input import img_folder
from pydicom.datadict import add_private_dict_entries
from custom_tag_mapper import custom_tags_dict,commands_to_run


class Conversion:
    """
    This class converts the .IMG image into DICOM
    series of images with metadata mapping.
    
    :param name: img_folder - Name of folder containing
    .img and Proprietory DICOMs
    :param type: str 
    
    """
    def __init__(self, img_folder):
        self.folder_name = img_folder
        self.dcm_tags = [[0x0028, 0x0008],
                    [0x0028, 0x0010],
                    [0x0028, 0x0011],
                    [0x0028, 0x0030],
                    [0x0018, 0x0088],
                    [0x0040, 0x0244],
                    [0x0040, 0x0245],
                    [0x0010, 0x0020],
                    [0x0010, 0x0010],
                    [0x0020, 0x0060]]
        self.dcm_tagnames = [
            "Number of Frames",
            "Rows",
            "Columns",
            "Pixel Spacing",
            "Spacing Between Slices",
            "Performed Procedure Step Start Date",
            "Performed Procedure Step Start Time",
            "Patient ID",
            "Patient's Name",
            "Laterality"]

        self.expected_frames = 128
        
    def main(self):
        """
        This method is starting point of execution. 
        It take no arguments and returns the convert method.
        
        :return: convert
        """
        # try:
        print("******")
        logging.basicConfig(filename='error_logs.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
        self.logger=logging.getLogger(__name__)
        print("###",img_folder)
        metadata_json_file = self.metadata_creation(img_folder)
        print(metadata_json_file)
        img_file = glob(img_folder +'\*.img')[0]
        print(img_file)
        print(self.convert(img_file,metadata_json_file))
        # except Exception as e:
            # self.logger.error("Exception in main") 
            # self.logger.error(e)
        
    def metadata_creation(self,img_folder):
        """
        This method used for creating the 
        metadata json from proprietory
        DICOM files. It return the json metadata 
        file.
        
        :param name: img_folder - Name of folder containing
        :param type: str 
        :return: json_file_path
       
       """
        try:
            list_dcms = glob(img_folder +'\*.DCM')
            list_dcms = sorted(list_dcms, key = os.path.getsize, reverse=True)
            total_tags = len(self.dcm_tags)
            for dcm_file in list_dcms:
                ds = dcmread(dcm_file)
                tags_present = [(tag in ds) for tag in self.dcm_tags]
                available_num_tags = np.sum(tags_present)
                if (available_num_tags==total_tags):
                    num_frames = str(ds[self.dcm_tags[0]].value)
                    elem = re.sub(r'[^\w]', '', num_frames)
                    elem = re.sub("[^0-9]", "", elem)
                    elem = int(elem)
                    
                    print("The propriatory DICOM file used for fetching metadata:",dcm_file)
                    # Rows
                    rows = int(ds[self.dcm_tags[1]].value)
                    # Columns
                    columns = int(ds[self.dcm_tags[2]].value)
                    # Pixel Spacing
                    pixel_spacing = str(ds[self.dcm_tags[3]].value)
                    pixel_spacing = re.sub(r'[^\x20-\x7e]', '', pixel_spacing)
                    pixel_spacing = re.sub("[^0-9,.]", "", pixel_spacing)
                    pixel_spacing_x = float(pixel_spacing.split(',')[0])
                    pixel_spacing_y = float(pixel_spacing.split(',')[1])
                    # Spacing between slices
                    pixel_spacing_z = str(ds[self.dcm_tags[4]].value)
                    pixel_spacing_z = re.sub(r'[^\x20-\x7e]', '', pixel_spacing_z)
                    pixel_spacing_z = re.sub("[^0-9,.]", "", pixel_spacing_z)
                    pixel_spacing_z = float(pixel_spacing_z)
                    # Study Date
                    study_date = str(ds[self.dcm_tags[5]].value)
                    study_date = re.sub("[^0-9]", "", study_date)
                    study_date = study_date[0:8]
                    # Study Time
                    study_time = str(ds[self.dcm_tags[6]].value)
                    study_time = re.sub("[^0-9,.]", "", study_time)
                    study_time = study_time[0:6]
                    # Patient ID
                    patient_id = str(ds[self.dcm_tags[7]].value)
                    patient_id = re.sub("[^0-9,.-]", "", patient_id)
                    patient_id = patient_id[0:10]
                    # Study ID
                    study_id = str(ds[self.dcm_tags[8]].value).split('^')[0]
                    # Laterality
                    laterality = str(ds[self.dcm_tags[9]].value)
                    laterality = re.sub(r'[^\x20-\x7e]', '', laterality)
                        
                
                    metadata_dict = {            
                                    "NumberOfFrames" :int(num_frames),
                                    "Rows": rows,
                                    "Columns":columns,
                                    "SpacingBetweenSlices":pixel_spacing_z,
                                    "PerformedProcedureStepStartDate":study_date,
                                    "PerformedProcedureStepStartTime":study_time,
                                    "PatientID": patient_id,
                                    "PatientName": "",
                                    "Laterality":laterality,
                                    "PixelSpacing": [pixel_spacing_x,pixel_spacing_y,pixel_spacing_z]
                                    }
                    json_file = str(img_folder) + ".json"
                    json_file_path = Path.joinpath(Path(img_folder), json_file)
                    with open(json_file_path, "w") as write_file:
                        json.dump(metadata_dict, write_file, indent=2)

                    print("Metadata created successfully")
                    break
                    
                
            return json_file_path
        
        except Exception as e:
            self.logger.error("Exception in metadata creation") 
            self.logger.error(e)  

    def convert(self,img_file,metadata_json_file):
        """
        This method is used for initialising the conversion
        
        :param name: img_file - name of the .img file
        :param type: str
        :param name: metadata_json_file - name of the Metadata json file
        :param type: str
    
        """
        try:
            self.img_filename = img_file
            self.json_file = metadata_json_file
            add_private_dict_entries("Novartis-NS", custom_tags_dict)
            self.custom_attributes = commands_to_run
            self.processing_file(img_file)
        except Exception as e:
            self.logger.error("Exception in convert") 
            self.logger.error(e)  
        
    def processing_file(self,img_filename):
        """
        This method is used for processing the conversion
        
        :param name: img_filename - name of the .img file for all slices
        :param type: str
        :return: mapping_json_metadata
    
        """
        try:
            #Reading the .img file
            with open(self.json_file) as json_file:
                metadata_dict = json.load(json_file)
            with open(img_filename, "rb") as fh :
                vol_bytes = np.frombuffer(bytearray(fh.read()), dtype=np.uint8)
                vol_bytes = vol_bytes.astype(np.int16)
            width = metadata_dict["Rows"]
            slices = metadata_dict["NumberOfFrames"]
            height = metadata_dict["Columns"]
            
            vol_array = np.reshape(vol_bytes, (slices, height, width))
            
            for s in range(slices):
                vol_array[s,:,:] = self.world_to_screen_coods(vol_array[s,:,:])
            new_img = sitk.GetImageFromArray(vol_array)
            
            pixel_spacing = metadata_dict["PixelSpacing"]
            new_img.SetSpacing(pixel_spacing)
            self.writer = sitk.ImageFileWriter()
            self.writer.KeepOriginalImageUIDOn()
            modification_time = time.strftime("%H%M%S")
            modification_date = time.strftime("%Y%m%d")
            # Mapping the DICOM values for all series headers
            series_tag_values = [
                                ("0020|000e", "1.2.840.10008.5.1.4.1.1.77.1.5.4.1.1"), # Series Instance UID
                                ("0008|0016","1.2.840.10008.5.1.4.1.1.77.1.5.4"),#SOP CLass Uid,
                                ("0020|000D","1.2.840.10008.5.1.4.1.1.77.1.5.4.2.1"),#study instance UID,,
                                ("0020|0052","1.2.840.10008.5.1.4.1.1.77.1.5.4." + modification_date + ".1"+ modification_time),#frame of referenceUID
                                ("0008|1030","Zeiss-OCT"),# Study Description 
                                ("0020|1209",""),#Number of series related instances
                                ("0020|0010","4d7dbe7e-d106-11ec-8992-e74f6a7a7b10"), #Study ID
                                ("0008|0050",""), #Accession Number 
                                ("0020|0011",""), #Series Number
                                ("0008|103E",""), #Series Description Attribute
                                ("0008|0005",""), # Specific Character Set Attribute
                                ("0008|0020",""), # Study Date  
                                ("0008|0030",""),  # Study Time
                                ("0008|0060","OCT") # Modality
                                ]   
            return self.mapping_json_metadata(series_tag_values,new_img)
        
        except Exception as e:
            self.logger.error("Exception in processing file") 
            self.logger.error(e)  
       
    def mapping_json_metadata(self,series_tag_values,new_img):
        """
        This method is used for mapping the json 
        metadata information into DICOM headers
        
        :param name: series_tag_values - Contains the list of attributes common for all slices
        :param type: list
        :param name: new_img - Image object
        :param type: simpleitk.image
    
        """
        try:
            if Path(self.json_file).is_file():
                with open(self.json_file) as json_file:
                    json_data = json.load(json_file)
                    
                csv_path =Path.joinpath(Path(__file__).parent, 'standard_tag_mapper.csv')
                mapperdf = pd.read_csv(csv_path)
                standard_attributes = list(mapperdf["Json_Attributes"])
                dicom_values = list(mapperdf["DICOM_tag"])
                dicom_tag_dict = dict(zip(standard_attributes,dicom_values))
                    
                self.commands = []
                for attribute_name,value in json_data.items():
                    if attribute_name in standard_attributes:
                        for attribute, dicom_tag in dicom_tag_dict.items():
                            if attribute_name == attribute and type(value)!= list:
                                series_tag_values.append((dicom_tag,str(value)))
                            if attribute_name == attribute and type(value) == list:
                                series_tag_values.append((dicom_tag,'\\'.join(map(str, [item for item in value]))))
                    elif attribute_name in self.custom_attributes.keys():
                        self.commands.append(self.custom_attributes[attribute_name].replace('value',str(value)))
                        
                    # Study specific values
                self.commands.append("block.add_new(0x10,'LO','RTH258')")
                self.commands.append("block.add_new(0x11,'LO','Eye')")   
                self.commands.append("block.add_new(0x12,'LO','AMD - age macular degeneration')")
                self.commands.append("block.add_new(0x13,'LO','')")
                self.commands.append("block.add_new(0x14,'LO','')") 
                self.commands.append("block.add_new(0x15,'LO','')")
                        
                for slice in tqdm(range(new_img.GetDepth())):
                    self.write_slices(series_tag_values, new_img, slice)
                    
        except Exception as e:
            self.logger.error("Exception in mapping json metadata") 
            self.logger.error(e)      
        
                
    
    def write_slices(self,series_tag_values, new_img, i):
        """
        This method is used for slice specific 
        information into header of slices.
        
        :param name: series_tag_values - Contains the list of attributes common for all slices
        :param type: list
        :param name: new_img - Image object
        :param name: i - Number of the slice
        :param type: int
       
        """
        try:
            output_file_name = "DICOM_" + str(self.folder_name)
            output = Path.joinpath(Path(img_folder), output_file_name)
            
            if not os.path.isdir(output):
                os.mkdir(output)
            
            image_slice = new_img[:,:,i]
            list(map(lambda tag_value: image_slice.SetMetaData(tag_value[0], tag_value[1]), series_tag_values))
            # Slice specific tags.
            image_slice.SetMetaData("0008|0018", "1.2.840.10008.5.1.4.1.1.77.1.5.4." + str(i))# SOP instance UID
            image_slice.SetMetaData("0008|0012", time.strftime("%Y%m%d")) # Instance Creation Date
            image_slice.SetMetaData("0008|0013", time.strftime("%H%M%S")) # Instance Creation Time
            image_slice.SetMetaData("0020|0032", '\\'.join(map(str,new_img.TransformIndexToPhysicalPoint((0,0,i))))) # Image Position (Patient)
            image_slice.SetMetaData("0020|0013", str(i))# Instance Number
            dicom_file_folder = os.path.join(output, "DICOM")
            
            return self.creating_dcm_files(dicom_file_folder,i,image_slice)
                
        except Exception as e:
            self.logger.error("Exception in write slices") 
            self.logger.error(e)          
    
    
    def creating_dcm_files(self,dicom_file_folder,i,image_slice):
        """
        This method is used for creating the dicom files.
        
        :param name: dicom_file_folder - Name of the DICOM 
         folder where all the DICOM files will present
        :param type: str
        :param name: i - number of slice
        :param type: int
        :param name: image_slice - Array of that slice
        :param type: np.ndarray
       
        """
        try:
            if not path.isdir(dicom_file_folder):
                    os.mkdir(dicom_file_folder)
            slice_name = str(i)+'.dcm'
            dcm_file_path = os.path.join(dicom_file_folder,slice_name) 
            self.writer.SetFileName(dcm_file_path)
            self.writer.Execute(image_slice)
            
            # Adding the private and custom tags
            dicom_file = dcmread(dcm_file_path, force = True)
            block = dicom_file.private_block(0x2013,'Novartis-NS',create =True)
            for command in self.commands:
                exec(command)
            dicom_file.save_as(dcm_file_path) 
                
           
            # file_path = os.path.join(dicom_file_folder,"Header_info_{}.txt".format(i)) 
            # sys.stdout = open(file_path, "w")
            # print(dicom_file)  
        except Exception as e:
            self.logger.error("Execption in creating dcm files") 
            self.logger.error(e) 
            
    def world_to_screen_coods(self,world_slice):
        """
        This method is used for flipping the image vertically.
        
        :param name: world_slice - Numpy array created from the .img image
        :param type: np.ndarray
        :return: numpy array (np.ndarray)
       
        """
         # flipping the image vertically
        try:
            rows = world_slice.shape[0]
            cols = world_slice.shape[1]
            screen_slice = np.zeros((rows,cols))
            for r in range(rows):
                screen_r = rows - r - 1
                screen_slice[screen_r,:] = world_slice[r,:]
            return screen_slice
        except Exception as e:
            self.logger.error("world to screen coods") 
            self.logger.error(e)  


    
    
if __name__ == "__main__":           
    conversion_object = Conversion(img_folder)
    conversion_object.main()

         
            
       

    


 

 
