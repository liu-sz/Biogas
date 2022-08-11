# Ecotone biogas meter reader
# Author: Shizhen Liu
# Date: August 2022

import cv2
import pytesseract
import csv
import os

"""
Directory structure
- read_meter.py
- processed_img.csv
- gas_meter_data.csv
- image
    - image_2022_8_6_1_29.jpg
    - image_2022_8_6_11_31.jpg
    - ...
"""

# Sync images from remote machine to local machine
source = " biogas@ecotone-biogas:/home/biogas/images/"
dest = " ~/path/to/local/image/folder"
cmd = "rsync -av --ignore-existing" + source + dest
os.system(cmd)

root = "full/path/to/image/folder/"

# List all image files in folder
image_folder = []
for (_, _, filenames) in os.walk(root):
    image_folder.extend(filenames)
    break

# Create processed_img.csv and writer header if it does not exist
if not os.path.exists('processed_img.csv'):   
    with open('processed_img.csv', 'a+') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['img'])

# Create gas_meter_data.csv and write header if it does not exist
fieldnames = ["year", "month", "day", "hour", "minute", "timestamp", "volume"]
if not os.path.exists('gas_meter_data.csv'):   
    with open('gas_meter_data.csv', 'a+') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(fieldnames)

# List all processed images
processed = []
with open('processed_img.csv', 'r') as processed_images:
    reader = csv.reader(processed_images, delimiter=',')
    for row in reader:
        processed.append(row[0])

# Remove processed images in image folder
for img in processed:
    if img in image_folder:
        image_folder.remove(img) 

# Parse image file name
def parse(path):
    filename = path.split('_')
    field_num = 6
    if len(filename) != field_num: return False
    
    year = filename[1]
    month = filename[2]
    day = filename[3]
    hour = filename[4]
    minute = (filename[5].split('.'))[0]
    date = year + '/' + month + '/' + day
    time = hour + ':' + minute + ':' + '00'
    timestamp = date + ' ' + time 
    
    entry = {
        "year": year, "month": month, "day": day,
        "hour": hour, "minute": minute,
        "timestamp": timestamp,
        "volume": None
    }
    return entry

# Read meter image
def read_meter(path, rows):
    entry = parse(path)
    if not entry: return None

    # Image processing
    # Reference: https://stackoverflow.com/questions/37745519/use-pytesseract-ocr-to-recognize-text-from-an-image
    img = cv2.imread(root + path)

    cropped_image = img[300:370, 160:560]
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # PSM 8 or 13 works well
    custom_config = r'--oem 3 --psm 13 -c tessedit_char_whitelist=0123456789'
    data = pytesseract.image_to_string(thresh, config=custom_config)
    ratio = 100
    reading = (int(data) // 10) / ratio;
    min = 50; max = 100;
    if not (reading < min or reading > max): 
        entry["volume"] = reading;
        rows.append(entry)
        print('Image: ', entry["timestamp"], 'Reading: ', reading)
    return reading

# Read images that have not been processed into rows
rows = []
for image in image_folder:
    try:
        read_meter(image, rows)
    except Exception as e:
        print(image, e)

# Append new data to CSV file
with open('gas_meter_data.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writerows(rows)

# Append processed images to csv file
with open('processed_img.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    for img in image_folder:
        writer.writerow([img])
