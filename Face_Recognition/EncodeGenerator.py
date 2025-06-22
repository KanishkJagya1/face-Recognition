import os
import cv2
import face_recognition
import pickle
import numpy as np
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recognition-db-58654-default-rtdb.firebaseio.com/"  # Replace with your Firebase Realtime DB URL
})

# Path to the image folder
folderPath = 'Images'
pathList = os.listdir(folderPath)
print("Found image files:", pathList)

imgList = []
studentIds = []

# Load images and extract student IDs
for path in pathList:
    img = cv2.imread(os.path.join(folderPath, path))
    imgList.append(img)
    studentIds.append(os.path.splitext(path)[0])

print("Student IDs:", studentIds)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes:
            encodeList.append(encodes[0])
        else:
            print("Warning: No face found in an image, skipping.")
    return encodeList

print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
print("Encoding Complete")

# Save encodings locally
encodeListKnownWithIds = [encodeListKnown, studentIds]
with open('EncodeFile.p', 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)

print("EncodeFile.p saved locally ✅")

# Upload encodings to Realtime DB
ref = db.reference('Encodings')
for encode, student_id in zip(encodeListKnown, studentIds):
    ref.child(student_id).set(encode.tolist())

print("Encodings uploaded to Firebase Realtime Database ✅")
