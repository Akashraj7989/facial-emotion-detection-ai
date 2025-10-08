# Facial Emotion Detection AI - Flask Web Application

A comprehensive facial emotion detection system using AI and deep learning, built with Flask, OpenCV, FER, and DeepFace libraries.

## Features

- **Image Upload Analysis**: Upload images to detect emotions with detailed confidence scores
- **Real-time Camera Detection**: Live emotion detection through webcam with real-time processing
- **Dual AI Models**: Uses both FER and DeepFace libraries for accurate emotion recognition
- **Modern Web Interface**: Beautiful, responsive Bootstrap-based UI
- **Multiple Emotions**: Detects Happy, Sad, Angry, Surprise, Fear, Disgust, and Neutral emotions
- **Visual Feedback**: Real-time bounding boxes and emotion labels on detected faces

## Supported Emotions

1. **Happy** 😊
2. **Sad** 😢  
3. **Angry** 😠
4. **Surprise** 😮
5. **Fear** 😨
6. **Disgust** 🤢
7. **Neutral** 😐

## Technology Stack

- **Backend**: Flask (Python web framework)
- **AI/ML Libraries**: 
  - FER (Facial Expression Recognition)
  - DeepFace (Deep learning facial analysis)
  - OpenCV (Computer vision)
  - TensorFlow (Deep learning backend)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Image Processing**: PIL, NumPy

## Installation & Setup

1. **Extract the zip file**:
   ```bash
   unzip facial_emotion_detection.zip
   cd facial_emotion_detection
   ```

2. **Install dependencies**:
   ```bash
   py -m pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   py app.py
   ```

4. **Access the application**:
   Open your browser and go to: `http://localhost:5000`

## Usage

### Image Upload Method
1. Click "Upload Image" from the home page
2. Select an image file (JPG, PNG, GIF, BMP)
3. Click "Detect Emotion" to analyze
4. View detailed results with confidence scores

### Live Camera Method
1. Click "Live Camera" from the home page
2. Click "Start Camera" to begin real-time detection
3. Position your face in front of the camera
4. See real-time emotion detection with bounding boxes
5. Click "Stop Camera" when done

## Project Structure

```
facial_emotion_detection/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── templates/            # HTML templates
    ├── base.html         # Base template with navigation
    ├── index.html        # Home page
    ├── upload.html       # Image upload page
    └── camera.html       # Live camera page
```

## API Endpoints

- `GET /` - Home page
- `GET /upload` - Image upload page
- `GET /camera` - Live camera page
- `POST /detect_emotion` - Analyze uploaded image
- `GET /start_camera` - Start camera for live detection
- `GET /stop_camera` - Stop camera
- `GET /video_feed` - Video stream endpoint

## Requirements

- Python 3.7+
- Webcam (for live detection)
- Internet connection (for initial model downloads)

## Models Used

1. **FER Library**: Uses pre-trained CNN models for emotion recognition
2. **DeepFace Library**: Leverages multiple deep learning architectures including VGG-Face

## Performance Notes

- Image processing typically takes 1-3 seconds
- Real-time detection runs at ~10 FPS
- GPU acceleration supported if TensorFlow-GPU is installed
- First run may take longer due to model downloads

## Troubleshooting

1. **Camera not working**: 
   - Ensure camera permissions are granted
   - Check if camera is being used by another application

2. **Slow performance**:
   - Close other applications using camera/CPU
   - Consider using tensorflow-gpu for better performance

3. **Installation issues**:
   - Make sure you're using Python 3.7+
   - Use virtual environment if facing dependency conflicts

## License

This project is open source and available under the MIT License.

## Credits

- FER Library by Justin Shenk
- DeepFace Library by Sefik Ilkin Serengil
- OpenCV Computer Vision Library
- Bootstrap for UI components

---

**Developed for educational and research purposes. Happy coding! 🚀**