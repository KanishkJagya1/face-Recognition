import os
import cv2
import numpy as np
import face_recognition
import pickle
from firebase_util import firebase_db  # assuming you have setup db in this module
from datetime import datetime
from encoderGenerator import EncoderGenerator

encoderGen = EncoderGenerator()
known_encodings = encoderGen.encodings


# Set path for the images folder
IMAGE_DIR = 'Images'
ENCODE_FILE_NAME = 'EncodeFile.p'

# Initialize containers
imgList = []
studentIDs = []

# Load all images from the folder
print("Scanning images...")
for filename in os.listdir(IMAGE_DIR):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        imgPath = os.path.join(IMAGE_DIR, filename)
        img = cv2.imread(imgPath)

        if img is None:
            print(f"[WARN] Unable to read image: {filename}")
            continue

        id = os.path.splitext(filename)[0]
        imgList.append(img)
        studentIDs.append(id)

print(f"Found {len(imgList)} valid image(s).")
print("Generating encodings...")

def generateEncodings(images):
    encodeList = []
    for idx, img in enumerate(images):
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Check for face(s)
        face_locations = face_recognition.face_locations(img)
        if not face_locations:
            print(f"[WARN] No face detected in image: {studentIDs[idx]}")
            continue

        # Generate encoding
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append((studentIDs[idx], encode))
        except Exception as e:
            print(f"[ERROR] Encoding failed for {studentIDs[idx]}: {e}")
    return encodeList

# Generate and pair encodings
encodings = generateEncodings(imgList)

# Save locally as pickle
print("Saving encodings locally...")
with open(ENCODE_FILE_NAME, 'wb') as file:
    data = {
        'encodings': [e[1] for e in encodings],
        'ids': [e[0] for e in encodings]
    }
    pickle.dump(data, file)

print("Encodings saved locally in EncodeFile.p")

# Upload to Firebase Realtime Database
print("Uploading encodings to Firebase...")
for student_id, encoding in encodings:
    encoding_list = encoding.tolist()  # Convert numpy array to JSON serializable list
    firebase_db.reference(f'Students/{student_id}').set({
        'encoding': encoding_list,
        'registered_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
print("Firebase upload complete.")
