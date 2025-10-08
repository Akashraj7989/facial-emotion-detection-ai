import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, render_template, Response
from fer import FER
from deepface import DeepFace
import base64
from PIL import Image
import io
import threading
import time

app = Flask(__name__)

# Initialize emotion detectors
fer_detector = FER(mtcnn=True)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Global variables for video streaming
camera = None
streaming = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/camera')
def camera_page():
    return render_template('camera.html')

@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Read and process the image
        img_bytes = file.read()
        np_img = np.frombuffer(img_bytes, np.uint8)
        image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({'error': 'Invalid image format'}), 400

        # Method 1: Using FER library
        fer_result = fer_detector.detect_emotions(image)
        fer_emotion, fer_score = fer_detector.top_emotion(image)

        # Method 2: Using DeepFace library
        try:
            deepface_result = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
            if isinstance(deepface_result, list):
                deepface_result = deepface_result[0]
            deepface_emotion = deepface_result['dominant_emotion']
            deepface_emotions = deepface_result['emotion']
        except Exception as e:
            deepface_emotion = "Could not detect"
            deepface_emotions = {}

        # Prepare response
        response = {
            'fer_emotion': fer_emotion if fer_emotion else 'No emotion detected',
            'fer_score': float(fer_score) if fer_score else 0.0,
            'fer_all_emotions': fer_result[0]['emotions'] if fer_result else {},
            'deepface_emotion': deepface_emotion,
            'deepface_emotions': deepface_emotions,
            'faces_detected': len(fer_result) if fer_result else 0
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

@app.route('/start_camera')
def start_camera():
    global camera, streaming
    try:
        if camera is None:
            camera = cv2.VideoCapture(0)
        streaming = True
        return jsonify({'status': 'Camera started'})
    except Exception as e:
        return jsonify({'error': f'Failed to start camera: {str(e)}'}), 500

@app.route('/stop_camera')
def stop_camera():
    global camera, streaming
    streaming = False
    if camera is not None:
        camera.release()
        camera = None
    return jsonify({'status': 'Camera stopped'})

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    global camera, streaming
    while streaming and camera is not None:
        try:
            success, frame = camera.read()
            if not success:
                break

            # Detect faces
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Process each face
            for (x, y, w, h) in faces:
                # Extract face region
                face_roi = frame[y:y+h, x:x+w]

                try:
                    # Get emotion using FER
                    emotion, score = fer_detector.top_emotion(face_roi)
                    if emotion:
                        # Draw rectangle around face
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                        # Add emotion text
                        emotion_text = f'{emotion}: {score:.2f}'
                        cv2.putText(frame, emotion_text, (x, y-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                except:
                    # Fallback: just draw rectangle
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.putText(frame, 'Processing...', (x, y-10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

            time.sleep(0.1)  # Add small delay

        except Exception as e:
            print(f"Error in generate_frames: {e}")
            break

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render uses dynamic ports
    app.run(host="0.0.0.0", port=port, debug=False)
