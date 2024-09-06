from django.shortcuts import render
from .forms import ImageUploadForm
from googletrans import Translator
import pytesseract
from PIL import Image, ImageOps
import cv2
import numpy as np
from io import BytesIO

def preprocess_image(image):
    img = np.array(image)
    if len(img.shape) == 3: 
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    elif len(img.shape) == 2:  
        pass
    else:
        raise ValueError("Unsupported image format")
    _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img

translator = Translator()

def image_upload(request):
    text = ''
    translated_text = ''
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            img = Image.open(image_file)

            # Ensure image is in RGB mode
            if img.mode != 'RGB':
                img = img.convert('RGB')

            img = preprocess_image(img)
            img = Image.fromarray(img)

            # Pass the PIL Image object directly to pytesseract
            text = pytesseract.image_to_string(img)
            translated_text = translator.translate(text, dest='hi').text

    else:
        form = ImageUploadForm()

    return render(request, 'ocr_app/upload.html', {
        'form': form,
        'text': text,
        'translated_text': translated_text
    })


# def image_upload(request):
#     text = ''
#     translated_text = ''
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             image_file = request.FILES['image']
#             img = Image.open(image_file)
#             if img.mode != 'RGB':
#                 img = img.convert('RGB')

#             img = preprocess_image(img)
#             img = Image.fromarray(img)  
#             img_byte_arr = BytesIO()
#             img.save(img_byte_arr, format='PNG')
#             img_byte_arr = BytesIO(img_byte_arr.getvalue())

#             text = pytesseract.image_to_string(img_byte_arr)
#             translated_text = translator.translate(text, dest='hi').text

#     else:
#         form = ImageUploadForm()

#     return render(request, 'ocr_app/upload.html', {
#         'form': form,
#         'text': text,
#         'translated_text': translated_text
#     })




# from django.shortcuts import render
# from .forms import ImageUploadForm
# from googletrans import Translator
# import pytesseract
# from PIL import Image, ImageOps
# import cv2
# import numpy as np
# from io import BytesIO

# translator = Translator()

# def preprocess_image(image):
#     img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
#     _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     return img

# def image_upload(request):
#     text = ''
#     translated_text = ''
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             image = request.FILES['image']
#             img = Image.open(image)
#             img = preprocess_image(img)
#             img = Image.fromarray(img)
#             text = pytesseract.image_to_string(img)
#             translated_text = translator.translate(text, dest='hi').text 

#     else:
#         form = ImageUploadForm()

#     return render(request, 'ocr_app/upload.html', {
#         'form': form,
#         'text': text,
#         'translated_text': translated_text
#     })
