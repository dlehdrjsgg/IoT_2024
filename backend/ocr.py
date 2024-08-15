from lib import *
import pytesseract
import numpy as np
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    alpha = 1.5
    beta = 0
    adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
    _, thresh = cv2.threshold(adjusted, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return processed

def find_number_regions(image):
    processed_image = preprocess_image(image)
    contours, _ = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    number_regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 20 and h > 20:
            number_regions.append((x, y, w, h))
    return number_regions

def extract_number_text(roi):
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789./-'
    text = pytesseract.image_to_string(roi, config=custom_config)
    return text.strip()

def extract_numeric_date(text):
    patterns = [
        r'\b\d{4}[-./]\d{2}[-./]\d{2}\b',  # 2024-10-21, 2024.10.21, 2024/10/21
        r'\b\d{2}[-./]\d{2}[-./]\d{4}\b',  # 21-10-2024, 21.10.2024, 21/10/2024
        r'\b\d{2}[-./]\d{2}[-./]\d{2}\b',  # 10-21-24, 10.21.24, 10/21/24
        r'\b\d{2}[-./]\d{2}\b',             # 10-21, 10.21
        r'\b\d{8}\b'                     # 20240815, 21102024
        r'\b\d{6}\b'                      # 211024
        r'\b\d{4}\b'
        r'\b\d{4}년 \d{2}월 \d{2}일\b'     # 2024년 10월 21일
        r'\b\d{2}월 \d{2}일 \d{4}년\b'     # 10월 21일 2024년
        r'\b\d{2}월 \d{2}일\b'             # 10월 21일
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group()
            only_digits = re.sub(r'\D', '', date_str)
            if len(only_digits) == 8:
                date = datetime.strptime(only_digits, '%Y%m%d').strftime('%Y-%m-%d')
            elif len(only_digits) == 6:
                date = datetime.strptime(only_digits, '%y%m%d').strftime('%Y-%m-%d')
            elif len(only_digits) == 4:
                date = datetime.strptime(only_digits, '%m%d').strftime('%Y-%m-%d')
            else:
                date = only_digits
            if (datetime.now() >= datetime.strptime(date, '%Y-%m-%d') or abs(datetime.now() - datetime.strptime(date, '%Y-%m-%d')).days > 730):
                return None
            return date
    return None

def process_frame(frame):
    number_regions = find_number_regions(frame)
    dates = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(extract_number_text, frame[y:y+h, x:x+w]) for (x, y, w, h) in number_regions]
        for future in futures:
            text = future.result()
            date = extract_numeric_date(text)
            if date:
                dates.append(date)
    
    return number_regions, dates

def main():
    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        number_regions, dates = process_frame(frame)
        if dates:
            log.Infolog("Detected dates: " + ', '.join(dates))
            break
        if debug:
            for (x, y, w, h) in number_regions:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('Date Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return dates[0]

if __name__ == "__main__":
    main()
