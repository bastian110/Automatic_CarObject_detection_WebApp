from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
from PIL import Image
from io import BytesIO
import base64
import cv2
import numpy as np

from models.machine_learning import PreprocessOnnx, ClassifyOnnx
from models.videoGestion import get_video_frames_classification, drawBoundingBoxesOnTheFrame

app = FastAPI()

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read Image
        # Read the UploadFile object as bytes
        image_bytes = await file.read()
        image = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        imagePreprocessed, original_size = PreprocessOnnx(image)
        # Classify the image
        outputs = ClassifyOnnx(imagePreprocessed, original_size)
        np_image = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        image = drawBoundingBoxesOnTheFrame(image, outputs)
        # Convert OpenCV Image (BGR) to PIL Image (RGB)
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        img_byte_arr = BytesIO()
        pil_image.save(img_byte_arr, format='PNG')
        modified_image_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        return JSONResponse(content={"modified_image_url": f"data:image/png;base64,{modified_image_base64}"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
