# main.py
import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import face_recognition
import numpy as np
from encoderGenerator import get_all_users, get_user_metadata, upload_user_metadata
import firebase_admin

# Initialize Camera
cap = cv2.VideoCapture(0)

# Main App Window
root = tk.Tk()
root.title("Face Recognition Login System")
root.geometry("800x600")

frame = tk.Label(root)
frame.pack()

# Global Variables
current_frame = None
known_encodings = {}  # username: encoding (numpy array)

def update_frame():
    global current_frame
    ret, img = cap.read()
    if ret:
        current_frame = img
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        img_pil = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img_pil)
        frame.imgtk = imgtk
        frame.configure(image=imgtk)
    root.after(10, update_frame)

def refresh_encodings():
    global known_encodings
    users = get_all_users()
    if users:
        for username, data in users.items():
            if 'encoding' in data:
                known_encodings[username] = np.array(data['encoding'])

refresh_encodings()

def login_user():
    if current_frame is None:
        messagebox.showerror("Error", "No frame captured!")
        return

    rgb_img = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_locations(rgb_img)
    encodings = face_recognition.face_encodings(rgb_img, faces)

    if not encodings:
        messagebox.showinfo("Face Not Found", "No face detected. Try again.")
        return

    user_encoding = encodings[0]
    for user, known_encoding in known_encodings.items():
        match = face_recognition.compare_faces([known_encoding], user_encoding, tolerance=0.45)
        if match[0]:
            messagebox.showinfo("Success", f"Welcome {user}")
            return

    messagebox.showwarning("Unknown", "User not found. Please register.")

def open_register_window():
    reg_win = tk.Toplevel(root)
    reg_win.geometry("600x400")
    reg_win.title("Register New User")

    tk.Label(reg_win, text="Enter Your Username:").pack(pady=10)
    username_entry = tk.Entry(reg_win)
    username_entry.pack(pady=5)

    def save_user():
        username = username_entry.get().strip()
        if not username or current_frame is None:
            messagebox.showerror("Error", "Username or frame invalid.")
            return

        rgb_img = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb_img)
        encodings = face_recognition.face_encodings(rgb_img, faces)

        if not encodings:
            messagebox.showwarning("Face Not Detected", "Try again.")
            return

        encoding = encodings[0].tolist()
        upload_user_metadata(username, {
            'encoding': encoding
        })
        known_encodings[username] = np.array(encoding)
        messagebox.showinfo("Registered", f"{username} registered successfully!")
        reg_win.destroy()

    tk.Button(reg_win, text="Accept", command=save_user).pack(pady=10)
    tk.Button(reg_win, text="Try Again", command=reg_win.destroy).pack(pady=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)
tk.Button(button_frame, text="Login", command=login_user, width=20, height=2).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Register new User", command=open_register_window, width=20, height=2).pack(side=tk.LEFT, padx=10)

update_frame()
root.mainloop()
cap.release()
