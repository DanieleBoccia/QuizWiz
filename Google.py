import re
import webbrowser
import cv2
import numpy as np
import pytesseract
from googlesearch import search
import tkinter as tk
from PIL import ImageGrab, ImageOps
import roi

# Configura pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata" --psm 6 -l ita'

def remove_special_chars(text):
    return ''.join(c for c in text if c.isalpha() or c.isspace())

def capture_screen(region):
    screenshot = ImageGrab.grab(bbox=region)
    return screenshot

def extract_text(image):
    text = pytesseract.image_to_string(image, config=tessdata_dir_config)
    print(text)
    return text

def extract_answers(text):
    pattern = r'\b[A-D]:\s*'
    answers = re.split(pattern, text)[1:]
    return answers

def google_search(query):
    results = []
    for j in search(query, num_results=10):
        results.append(j)
    return results

def count_occurrences(text, answers):
    occurrences = []
    for answer in answers:
        count = text.lower().count(answer.lower())
        occurrences.append((answer, count))
    return occurrences

def show_popup(occurrences):
    window = tk.Tk()
    window.title("Risultati")

    for i, (answer, count) in enumerate(occurrences):
        label = tk.Label(window, text=f"{i + 1}. {answer}: {count} occorrenze")
        label.pack()

    window.mainloop()

def open_browser_with_question(question):
    url = f"https://www.google.com/search?q={question}"
    webbrowser.open(url)

def main():
    # Definisci la regione dello schermo da catturare (x, y, larghezza, altezza)
    question_region = (0, 600, 800, 700)
    answers_region = (0, 700, 800, 900)

    question_screenshot = capture_screen(question_region)
    question_text = extract_text(question_screenshot)
    question_text = remove_special_chars(question_text)
    
    answers_screenshot = capture_screen(answers_region)
    answers_text = extract_text(answers_screenshot)
    answers_text = remove_special_chars(answers_text)
    answers = extract_answers(answers_text)
    answers = answers_text.splitlines()

    browser = open_browser_with_question(question_text)

    search_results = google_search(question_text)
    search_text = " ".join(search_results)

    occurrences = count_occurrences(search_text, answers)
    occurrences.sort(key=lambda x: x[1], reverse=True)

    show_popup(occurrences)

if __name__ == "__main__":
    main()



