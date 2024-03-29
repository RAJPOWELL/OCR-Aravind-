from flask import Flask, render_template, request
import cv2
import pytesseract
import numpy as np

app = Flask(__name__)

# Set path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Define keywords to identify fields
field_keywords = {
    'name': ['الاسم'],
    'address': ['اسم الاب'],
    'dob': ['تاريخ الولادة']
}

def perform_ocr(img):
    text = pytesseract.image_to_string(img, lang="ara")
    data = {}
    for field, keywords in field_keywords.items():
        for keyword in keywords:
            if keyword in text.lower():
                start_index = text.lower().index(keyword)
                end_index = start_index + len(keyword)
                actual_text = text[end_index:].strip()
                data[field] = actual_text[:end_index].strip()
                break
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get uploaded file
        file = request.files['file']
        # Read the image
        img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
        # Perform OCR
        extracted_data = perform_ocr(img)
        return render_template('result.html', data=extracted_data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
