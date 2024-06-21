import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

# Specify the path to the Tesseract executable if not in your PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\sahana\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

class ImageProcessor:
    def __init__(self):
        pass

    def preprocess_image(self, image):
        # Convert to grayscale
        image = image.convert('L')

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)  # Increase contrast

        # Apply median filter
        image = image.filter(ImageFilter.MedianFilter())

        # Apply Gaussian blur
        image = image.filter(ImageFilter.GaussianBlur(radius=1))

        return image

    def extract_text(self, image):
        processed_image = self.preprocess_image(image)
        custom_config = r'--oem 3 --psm 6'  # Specify OCR Engine Mode and PSM
        text = pytesseract.image_to_string(processed_image, config=custom_config)
        
        # Clean up extracted text
        cleaned_text = ' '.join(text.strip().split())  # Remove extra spaces and join lines
        return cleaned_text

def main():
    st.title("Image Text Extractor")

    st.sidebar.header("Select Image")
    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image_processor = ImageProcessor()

        # Display the selected image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        # Check if user clicked the 'Extract Text' button
        if st.button('Extract Text'):
            text = image_processor.extract_text(image)
            st.write('### Extracted Text:')
            st.write(text)  # Display extracted text

if __name__ == '__main__':
    main()
