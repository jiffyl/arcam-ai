
from flask import Flask, render_template, request, redirect, url_for, flash
import face_recognition
import os
import cv2
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'supersecretkey'

# Load known faces
known_face_encodings = []
known_face_names = []

for filename in os.listdir('known_faces'):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join('known_faces', filename)
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_face_encodings.append(encoding[0])
            known_face_names.append(os.path.splitext(filename)[0])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        if not file:
            flash("No file selected.")
            return redirect(url_for('index'))

        img = face_recognition.load_image_file(file)
        unknown_encodings = face_recognition.face_encodings(img)

        if not unknown_encodings:
            flash("No face detected in uploaded image.")
            return redirect(url_for('index'))

        unknown_encoding = unknown_encodings[0]
        results = face_recognition.compare_faces(known_face_encodings, unknown_encoding)

        for i, match in enumerate(results):
            if match:
                flash(f"Match found: {known_face_names[i]}")
                break
        else:
            flash("No match found.")

        return redirect(url_for('index'))

    return render_template('index.html')  # This is your GET handler

