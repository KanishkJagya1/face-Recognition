import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://face-recognition-db-58654-default-rtdb.firebaseio.com/'
})


ref = db.reference('Students')
from datetime import datetime

data = {
    "1": {
        "name": "Akarsh Srivastava",
        "major": "Robotics",
        "starting_year": 2021,
        "total_attendance": 15,
        "standing": "A",
        "year": 3,
        "last_attendance_time": str(datetime.now())
    },
    "2": {
        "name": "Gopal Aggarwal",
        "major": "Computer Science",
        "starting_year": 2022,
        "total_attendance": 12,
        "standing": "B",
        "year": 2,
        "last_attendance_time": str(datetime.now())
    },
    "3": {
        "name": "Gurman Kaur",
        "major": "Electrical Engineering",
        "starting_year": 2020,
        "total_attendance": 20,
        "standing": "A",
        "year": 4,
        "last_attendance_time": str(datetime.now())
    },
    "4": {
        "name": "Hushraj Singh",
        "major": "Mechanical Engineering",
        "starting_year": 2023,
        "total_attendance": 9,
        "standing": "C",
        "year": 1,
        "last_attendance_time": str(datetime.now())
    },
    "5": {
        "name": "Jasdeep Singh",
        "major": "Civil Engineering",
        "starting_year": 2021,
        "total_attendance": 11,
        "standing": "B",
        "year": 3,
        "last_attendance_time": str(datetime.now())
    },
    "6": {
        "name": "Pancham Agarwal",
        "major": "Artificial Intelligence",
        "starting_year": 2022,
        "total_attendance": 17,
        "standing": "A",
        "year": 2,
        "last_attendance_time": str(datetime.now())
    },
    "7": {
        "name": "Pariansh Mahajan",
        "major": "Data Science",
        "starting_year": 2020,
        "total_attendance": 14,
        "standing": "G",
        "year": 4,
        "last_attendance_time": str(datetime.now())
    },
    "8": {
        "name": "Sparsh Rastogi",
        "major": "Cybersecurity",
        "starting_year": 2023,
        "total_attendance": 8,
        "standing": "C",
        "year": 1,
        "last_attendance_time": str(datetime.now())
    }
}

for key, value in data.items():
    ref.child(key).set(value)