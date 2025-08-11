# DICOM Redactor

A simple, local tool for anonymizing DICOM images by removing burned-in patient health information (PHI) using OCR and metadata redaction.

📖 Read the Full Story

Want to learn more about the motivation, design, and technical details behind this project? Check out the accompanying Medium article:

👉 [Read on Medium] https://medium.com/@mithilesh007/anonymizing-dicom-images-with-ocr-and-inpainting-a-simple-local-tool-for-researchers-dd59c54d59ce 

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
```

## 🛠️ Usage

```python
from redactor import TextRedactor

redactor = TextRedactor(
    dicom_dir='path/to/input_dicoms',
    output_dir='path/to/output_dicoms',
    csv_file_path='path/to/tags_to_remove.csv'
)
redactor.process_dicom_files()
```

## 📁 Example Datasets

Two synthetic datasets are included in the `examples/` folder. These were created using an online JPEG-to-DICOM converter and a CT background image from Wikimedia Commons.

## ⚠️ Notes

- **Performance**: Works best when text and regions of interest are spatially separated.
- **Inpainting**: May alter regions of interest—manual review is recommended before distribution.
- **Hardware**: GPU is recommended for faster OCR processing. CPU works but is slower.
- **Customization**: You can tailor image handling and metadata redaction to suit your own use case.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🤝 Contributing

Feel free to fork, modify, and submit pull requests. Suggestions and improvements are welcome!
