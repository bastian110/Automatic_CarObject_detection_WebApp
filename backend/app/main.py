from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse, Response

import numpy as np
import cv2

from machine_learning import PreprocessOnnx, ClassifyOnnx
from videoGestion import get_video_frames_classification, drawBoundingBoxesOnTheFrame

app = FastAPI()


@app.post("/classify-picture/")
async def classify_uploaded_image(file: UploadFile):
    try:
        # Read the UploadFile object as bytes
        image_bytes = await file.read()
        image = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        imagePreprocessed, original_size = PreprocessOnnx(image)
        # Classify the image
        outputs = ClassifyOnnx(imagePreprocessed, original_size)
        print('test')
        print(outputs)
        np_image = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        image = drawBoundingBoxesOnTheFrame(image, outputs)
        cv2.imwrite('test.jpg', image)
        # Return the classification result as JSON
        return StreamingResponse(content=image, status_code=200)
                                 
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



some_file_path = "/Users/bastianchuttarsing/Downloads/traffic1.mp4"

@app.get("/read_video")
async def read_video():
    try:
        async def generate_frames():
            # Open the video file
            cap = cv2.VideoCapture(some_file_path)
            while True:
                # Read a frame from the video
                ret, frame = cap.read()
                if not ret:
                    break
                frame_preprocessed, original_size = PreprocessOnnx(frame)
                outputs = ClassifyOnnx(frame_preprocessed, original_size)
        
                frame = drawBoundingBoxesOnTheFrame(frame, outputs)
                cv2.imwrite('TEST.jpg', frame)
                # Convert the frame to JPEG format
                _, jpeg = cv2.imencode('.jpg', frame)
                # Yield the frame as bytes
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)    
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace;boundary=frame")


@app.get("/webcam-classification")
def read_webcam():
    def generate_frames():
        # Open the video file
        cap = cv2.VideoCapture(0)
        while True:
            # Read a frame from the video
            ret, frame = cap.read()
            if not ret:
                break
            frame_preprocessed, original_size = PreprocessOnnx(frame)
            print('TEST MAIN')
            outputs = ClassifyOnnx(frame_preprocessed, original_size)
    
            frame = drawBoundingBoxesOnTheFrame(frame, outputs)
            cv2.imwrite('TEST.jpg', frame)
            print('SHAPE FRAME', frame[0].shape)
            # Convert the frame to JPEG format
            _, jpeg = cv2.imencode('.jpg', frame)
            # Yield the frame as bytes
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace;boundary=frame")
