import pytesseract
import cv2
import os

def perform_ocr(img_path):
    
    text = pytesseract.image_to_string(img_path, lang='ara', config='--tessdata-dir "/usr/share/tesseract-ocr/4.00/tessdata/"')
     
    # Set TESSDATA_PREFIX environment variable
    os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/4.00/'

    # Set path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
    
    # Read the input image
    try:
        img = cv2.imread("/home/raj/Temp/Aravind/for raj/flags/5.jpg")
        if img is None:
            raise ValueError("Unable to load image")
    except Exception as e:
        return {"error": str(e)}
    
    # Perform OCR on the image
    try:
        text = pytesseract.image_to_string(img, lang="ara")
    except Exception as e:
        return {"error": str(e)}
    
    # Define keywords to identify fields
    field_keywords = {
        'name': ['الاسم'],
        'address': ['اسم الاب'],
        'dob': ['تاريخ الولادة']
    }
    
    # Extract specific fields based on keywords
    data = {}
    for field, keywords in field_keywords.items():
        for keyword in keywords:
            if keyword in text.lower():
                start_index = text.lower().index(keyword)
                end_index = start_index + len(keyword)
                actual_text = text[end_index:].strip()
                data[field] = actual_text[:end_index].strip()
                break
    
    # Return the extracted data
    return data
