import cv2
import numpy as np
import serial
import time
import threading

# Constants
TRIGGER_RECOVERY_TIME_SEC   = 5.0            # only fire every X seconds
TRIGGER_CLASS               = 15             # 0 = person, 15 = cat, 16 = dog, 46 = banana, 47 = apple, 49 = orange
TRIGGER_MIN_AREA            = 1000           # Min. change in image to start object detection
WEBCAM_INDEX                = 0              # Index of installed webcams
TRIGGER_BAUDRATE            = 9600           # Arduino baudrate
TRIGGER_SERIAL              = '/dev/ttyACM0' # Serial port for Arduino connection
TRIGGER_SERIAL_COMMAND      = "FIRE!\n"      # ASCII command to activate Arduino
MIN_CONFIDENCE              = 0.50           # Min. confidence in object detection (to draw a rectangle)
TRIGGER_MIN_CONFIDENCE      = 0.75           # Min. confidence to actually fire
WINDOW_TITLE                = "YOLO SENTRY"  # Text for window title
SAVE_VIDEO                  = True           # Write frames to an output video file
SAVE_VIDEO_FILE             = "output.avi"   # File for output video. this will get overwritten on each restart
SAVE_VIDEO_FPS              = 10.0           # Frames per second for output video

# yolo can detect a lot of classes, but
# only put a rectangle on classes in this list:
list_of_marked_objects = [ TRIGGER_CLASS ]

# Load Yolo (neural network to classify objects in image)
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# load the COCO class labels the YOLO model was trained on
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Open webcam stream
try:
    cap = cv2.VideoCapture(WEBCAM_INDEX)
except Exception as e:
    print("Failed to open webcam")
    quit()

cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)

# Open actuator serial stream (Arduino)
try:
    ser = serial.Serial(TRIGGER_SERIAL, TRIGGER_BAUDRATE)  # adjust baud rate if required
    trigger_enabled = True
except serial.SerialException as e:
    print("Could not open serial port %s. Actuator not enabled." % TRIGGER_SERIAL)
    trigger_enabled = False

# time keeping
timestamp_last_ser_cmd = time.time() # timestamp of last fire command
timestamp_fps = time.time()          # for the FPS counter
frame_counter = 0                    # for the FPS counter

# open a video file to save the stream
if SAVE_VIDEO:
    _, frame = cap.read()
    height, width, channels = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_out = cv2.VideoWriter(SAVE_VIDEO_FILE, fourcc, SAVE_VIDEO_FPS, (width, height))

ret, prev_frame = cap.read()

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    height, width, channels = frame.shape
    frame_counter += 1

    if time.time() - timestamp_fps >= 1.0:
        timestamp_fps = time.time()
        print("\rFPS: %i" % (frame_counter), end="") # return cursor to beginning of line
        frame_counter = 0

    diff = cv2.absdiff(frame, prev_frame)
    prev_frame = frame
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) # Convert the difference to grayscale
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY) # Apply a binary threshold to the grayscale image
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Find contours in the thresholded image
    # Filter contours based on area
    significant_change_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > TRIGGER_MIN_AREA:
            significant_change_detected = True

    if significant_change_detected:
        # Detecting objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        class_ids = []
        confidences = []
        boxes = []

        # Showing detected objects in webcam live image
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > MIN_CONFIDENCE and class_id in list_of_marked_objects:
                    # Object detected, save coordinates for drawing a rectangle
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

                    # Send actuator command if conditions are met
                    if (confidence > TRIGGER_MIN_CONFIDENCE and
                        class_id == TRIGGER_CLASS and
                        time.time() - timestamp_last_ser_cmd > TRIGGER_RECOVERY_TIME_SEC and
                        trigger_enabled):
                        msg = TRIGGER_SERIAL_COMMAND
                        ser.write(msg.encode())
                        timestamp_last_ser_cmd = time.time()
                        if SAVE_VIDEO:
                            video_out.write(frame)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                confidence_percent = confidences[i] * 100
                label = f"{str(classes[class_ids[i]])} {confidence_percent:.1f}%"
                color = colors[i]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y + 30), font, 2, color, 3)

    if cv2.getWindowProperty(WINDOW_TITLE, cv2.WND_PROP_VISIBLE) < 1:
        break
    cv2.imshow(WINDOW_TITLE, frame)
    key = cv2.waitKey(1)
    if key == 27:  # if ESC is pressed, the loop will stop
        break

cap.release()
cv2.destroyAllWindows()
if trigger_enabled:
    ser.close()
if SAVE_VIDEO:
    video_out.release()

