from ultralytics import YOLO
from ultralytics.utils.ops import non_max_suppression, xyxy2xywh
import onnx
import onnxruntime as ort
import cv2
import numpy as np
import torch
model = ort.InferenceSession("models/yolov8m.onnx")
#model = YOLO('/Users/bastianchuttarsing/Documents/CarObject_detection/ml_models/yolov8m.pt',task='detect')
model_classnames = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}

def PreprocessOnnx(image):

    original_size = image.shape[:2][::-1]
    print('TEST VIDEO')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (640, 640), interpolation=cv2.INTER_AREA)
    image = image.transpose(2, 0, 1)
    image = image.astype(np.float32)
    image /= 255.0
    image = np.expand_dims(image, axis=0)
    return image, original_size


def ClassifyOnnx(image, original_size):
    """
    Return (x1, y1, x2, y2, conf, cls_pred) for each bounding box detected
    """
    input_name = model.get_inputs()[0].name
    print(model.get_inputs())
    output_name = model.get_outputs()[0].name
    # sess = ort.InferenceSession(model.SerializeToString())
    outputs = model.run([output_name], {input_name: image})
    outputs = torch.from_numpy(np.asarray(outputs))
    outputs = non_max_suppression(
        outputs[0], conf_thres=0.4, max_det=100, agnostic=True)[0]
    
    outputs[:, 0] = outputs[:, 0] * original_size[0] / 640
    outputs[:, 1] = outputs[:, 1] * original_size[1] / 640
    outputs[:, 2] = outputs[:, 2] * original_size[0] / 640
    outputs[:, 3] = outputs[:, 3] * original_size[1] / 640

    return outputs
