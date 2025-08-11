# Example DICOM Files

This folder contains synthetic DICOM files used to demonstrate the functionality of the DICOM Redactor tool.

## 📁 Files

- `own-test-001.dcm`
- `own-test-001-1.dcm`

These are synthetic DICOM images created using an online JPEG-to-DICOM converter. The background CT image was sourced from Wikimedia Commons. These files contain simulated patient health information (PHI) burned into the image to mimic real-world scenarios.

- `own-test-001_redacted.dcm`
- `own-test-001-1_redacted.dcm`

These are the redacted versions of the above files. The DICOM Redactor tool has:
- Detected and removed visible text using Keras-OCR.
- Inpainted the text regions to obscure PHI.
- Redacted sensitive metadata tags based on a CSV configuration.

## 📝 Notes

- The tool performs best when the region of interest and text are spatially separated.
- Inpainting may alter the image, especially near text regions. Manual review is recommended before distribution.
- GPU acceleration is recommended for faster OCR processing. CPU is supported but slower.
- The redaction process is customizable for different use cases.
