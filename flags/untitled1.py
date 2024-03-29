import pytesseract as tess
from PIL import Image

img = Image.open('C:\Users\MY PC\Desktop\flags\5.jpg')
text = tess.image_to_string(img)

print(text)
