import cv2
from .machine_learning import PreprocessOnnx, ClassifyOnnx, model_classnames



def get_video_frames_classification(video_path):
    # Open the video file
    print('cap:  ')
    cap = cv2.VideoCapture(video_path)
    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret:
            break
        frame = PreprocessOnnx(frame)
        bounding_boxes_coordinates = ClassifyOnnx(frame)
        frame = drawBoundingBoxesOnTheFrame(frame, bounding_boxes_coordinates)
        # Convert the frame to JPEG format
        _, jpeg = cv2.imencode('.jpg', frame)
        # Yield the frame as bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

def drawBoundingBoxesOnTheFrame(frame, bounding_boxes_coordinates):
    # draw rectangles and labels on the original image
    
    if frame is not None:
        for box in bounding_boxes_coordinates:
            box = box.cpu().numpy()
            x1, y1, x2, y2, conf, cls_pred = box
            print(x1, y1, x2, y2)
            x1 = int(x1)
            x2 = int(x2)
            y1 = int(y1)
            y2 = int(y2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, str(str(model_classnames[int(cls_pred)])), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    else:
        print('No frame')
    return frame