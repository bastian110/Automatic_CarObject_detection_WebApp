# Car Detector with YOLOv5

## Description
This web application leverages the YOLOv5 pre-trained model for real-time car segmentation and detection within images or streamed videos. Built with Flask, it provides an easy-to-use API for processing user-uploaded images or video streams, identifying and segmenting cars with high accuracy. This project demonstrates the application of advanced computer vision techniques in practical, real-world scenarios.

## Installation

### Prerequisites
- Python 3.8+
- Flask
- React.js
- PyTorch
- Onnx

### Setup
1. Clone the repository:
```bash
git clone bastian110/Automatic_CarObject_detection_WebApp
```

Install React dependencies:
```bash
cd frontend
npm install
```


### Usage

Running the Application
Start the Flask server:
```bash
flask run
```

Launching the Frontend Application
In a separate terminal, navigate to the React application directory and execute:

```bash
npm start
```
The web application should now be accessible through your browser.

### Uploading Images or Streaming Video
To analyze an image, navigate to the image upload section and select an image file.
For video stream analysis, ensure your video source is correctly configured and accessible by the application.

## Features
Real-time car detection and segmentation in images and video streams.
Easy-to-use web interface for uploading images and streaming video.
Utilization of the YOLOv5 model for accurate and efficient object detection.
Technologies Used

Backend: Flask API
Frontend: React.js
Machine Learning and Computer Vision: YOLOv5 & ONNX
