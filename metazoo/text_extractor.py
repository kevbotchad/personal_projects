# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# C:\Users\Kevbo\OneDrive\Desktop\Coding\personal_projects\metazoo\cards_images\cards
# C:\Users\Kevbo\OneDrive\Desktop\Coding\personal_projects\metazoo\extracted_card_data.json

import os
import cv2
import pytesseract
import numpy as np
from PIL import Image

import os
import cv2
import pytesseract
from PIL import Image

# Paths to your input images and output text files
input_folder = r"C:\Users\Kevbo\OneDrive\Desktop\Coding\personal_projects\metazoo\cards_images\cards"

# Optional: Set Tesseract command path if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        image_path = os.path.join(input_folder, filename)
        img = cv2.imread(image_path)
        if img is None:
            print(f"Failed to read {filename}")
            continue

        # Convert to grayscale and resize for better OCR accuracy
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        # Apply thresholding (you might need to adjust or remove this step based on your images)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # Example cropping regions (y1:y2, x1:x2)
        # Adjust these coordinates based on where each element is on your card.
        card_name_region = thresh[0:100, 0:800]      # Top region for the card name
        beastie_tribe_region = thresh[90:150, 50:400]   # Next region for beastie tribe text
        lp_region = thresh[160:220, 50:400]             # Region for LP
        spellbook_region = thresh[230:290, 50:400]      # Region for spellbook info (if applicable)

        # Use Tesseract on each cropped region
        # Using psm 7 (treat image as a single text line) can be useful for small text segments
        config = "--psm 7"
        card_name_text = pytesseract.image_to_string(Image.fromarray(card_name_region), lang="eng", config=config)
        beastie_tribe_text = pytesseract.image_to_string(Image.fromarray(beastie_tribe_region), lang="eng", config=config)
        lp_text = pytesseract.image_to_string(Image.fromarray(lp_region), lang="eng", config=config)
        spellbook_text = pytesseract.image_to_string(Image.fromarray(spellbook_region), lang="eng", config=config)

        print("Card Name:\n")
        print(card_name_text.strip() + "\n\n")
        print("Beastie Tribe:\n")
        print(beastie_tribe_text.strip() + "\n\n")
        print("LP:\n")
        print(lp_text.strip() + "\n\n")
        print("Spellbook:\n")
        print(spellbook_text.strip() + "\n\n")
        break

