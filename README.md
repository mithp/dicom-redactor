# DICOM Redactor

A simple, local tool for anonymizing DICOM images by removing burned-in patient health information (PHI) using OCR and metadata redaction.

## 🧠 Motivation

DICOM is a standard format used in healthcare to store and analyze image data. Sometimes, patient information is embedded directly into the image (burned-in), which poses challenges when using these images for secondary purposes like research.

This tool provides a naive but effective way to handle such cases locally using OCR-based detection and inpainting.

## 🚀 Features

- Detects and removes visible text using Keras-OCR
- Redacts sensitive metadata tags based on a CSV configuration
- Processes `.dcm` and `.dicom` files in a given folder
- Saves redacted images in a separate output folder
- Easy to customize for your own post-processing needs

## 📦 Installation

```bash
pip install -r requirements.txt
