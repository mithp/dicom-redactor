# ------------------------------------------------------------------------------
# TextRedactor: A tool for redacting PHI from DICOM files
#
# This script processes DICOM images to:
# 1. Detect and inpaint text burned into the image using kerasOCR.
# 2. Replace sensitive metadata fields (e.g., patient name, ID) with "REDACTED"
#    based on a configurable CSV file listing DICOM tags and redaction flags.
#
# Usage:
# - Provide input and output directories for DICOM files.
# - Supply a CSV file with tags to redact in the format: tag (e.g., 0x0010,0x0010), delete (True/False).
#
# Dependencies: pydicom, keras_ocr, OpenCV, NumPy
# ------------------------------------------------------------------------------

import os
import glob
import cv2
import numpy as np
import pydicom
import keras_ocr
import csv
#import matplotlib.pyplot as plt

class TextRedactor:
    def __init__(self, dicom_dir, output_dir, csv_file_path):
        # Initialize the TextRedactor class with directories for DICOM files and output
        self.dicom_dir = dicom_dir
        self.output_dir = output_dir
        self.csv_file_path = csv_file_path
        # Create the output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        # Initialize the OCR pipeline from keras_ocr
        self.pipeline = keras_ocr.pipeline.Pipeline()
        # Load tags to remove from CSV file
        self.tags_to_remove = self.load_tags_from_csv()

    def load_tags_from_csv(self):
        tags_to_remove = []
        with open(self.csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                tag_str = row[0]
                tag_parts = tag_str.split(',')
                tag = (int(tag_parts[0], 16), int(tag_parts[1], 16))
                delete = row[1].lower() == 'true'
                if delete:
                    tags_to_remove.append(tag)
        return tags_to_remove
    
    @staticmethod
    def inpaint_text(image, predictions):
        # Create a mask for the text areas to be inpainted
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
    
        # Loop through the OCR predictions and create rectangles on the mask
        for _, box in predictions[0]:
            x_coords = [int(pt[0]) for pt in box]
            y_coords = [int(pt[1]) for pt in box]
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            cv2.rectangle(mask, (x_min, y_min), (x_max, y_max), 255, -1)
    
        # Inpaint the text areas using the mask
        return cv2.inpaint(image, mask, inpaintRadius=7, flags=cv2.INPAINT_NS)

    def replace_metadata(self, dicom):
        # Replace the tags with "REDACTED"
        for tag in self.tags_to_remove:
            if tag in dicom:
                dicom[tag].value = "REDACTED"

    
    def process_dicom_files(self):
        dicom_files = glob.glob(os.path.join(self.dicom_dir, "*.dcm")) + glob.glob(os.path.join(self.dicom_dir, "*.dicom"))
        
        for file_path in dicom_files:
            ext = os.path.splitext(file_path)[1]
            try:
                ds = pydicom.dcmread(file_path)
                if 'PixelData' not in ds:
                    continue
                # Original pixel array
                pixel_array = ds.pixel_array
    
                # Normalize and convert to RGB
                norm_img = cv2.normalize(pixel_array, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
                rgb_img = cv2.cvtColor(norm_img, cv2.COLOR_GRAY2RGB)
    
                # OCR and inpainting
                predictions = self.pipeline.recognize([rgb_img])
                redacted_img = self.inpaint_text(rgb_img, predictions)
                
                #Sanity check
                #plt.imshow(redacted_img)
    
                # Extract red channel and cast to original pixel type
                pixel_data_de_phi = redacted_img[:, :, 0].astype(ds.pixel_array.dtype)
                
                
                ds.Rows, ds.Columns = pixel_data_de_phi.shape
                ds.SamplesPerPixel = 1
                ds.PhotometricInterpretation = "MONOCHROME2"
                ds.BitsAllocated = ds.pixel_array.dtype.itemsize * 8
                ds.BitsStored = ds.BitsAllocated
                ds.HighBit = ds.BitsStored - 1
                ds.PixelRepresentation = ds.get("PixelRepresentation", 0)
                
                ds.PixelData = pixel_data_de_phi.tobytes()
                ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
    
                # Replace metadata if needed
                self.replace_metadata(ds)
    
                # Save redacted file
                output_path = os.path.join(self.output_dir, os.path.basename(file_path).replace(ext, f"_redacted{ext}"))
                ds.save_as(output_path, write_like_original=False)
    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

# Example usage
#%%

redactor = TextRedactor(dicom_dir='path/input_dicoms', 
                        output_dir='path/output_dicoms', 
                        csv_file_path= 'path/tags_to_remove.csv')
redactor.process_dicom_files()
