from networktables import NetworkTables
from grip import LemonVisionGripPipeline
from red_grip import RedBlobPipeline

import config

import cv2
import time
import math
import threading


def calculate_coords(frame_width, frame_height, x_cam_coord, y_cam_coord):
    cx = frame_width / 2 - 0.5
    cy = frame_height / 2 - 0.5

    pitch_angle = math.atan(y_cam_coord - cy) / config.focal_len
    yaw_angle = math.atan(x_cam_coord - cx) / config.focal_len

    #print("pitch angle: " + str(pitch_angle))
    #print("yaw angle: " + str(yaw_angle))

    return pitch_angle, yaw_angle


# Start thread to connect to NetworkTables
cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

# Use RoboRIO static IP address
NetworkTables.initialize(server=config.nt_ip) # Don't use 'roborio-192-frc.local'. https://robotpy.readthedocs.io/en/stable/guide/nt.html#networktables-guide
# NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

# with cond:
    # print("Waiting")
    #if not notified[0]:
        #cond.wait()

print("Connected to NetworkTables!")

# Initialize Jetson NetworkTable
table = NetworkTables.getTable(config.nt_name)

# Read camera frames
input_port = 0
num_ports = 4

cap = cv2.VideoCapture(input_port)
_, frame = cap.read()

# Keep trying until image is obtained
while frame is None:

    print("Error: No image to process. Cannot run vision pipeline. Are images being captured from the camera?")

    # Try a different port
    input_port = (input_port + 1) % num_ports
    cap = cv2.VideoCapture(input_port)

    # Read frame
    _, frame = cap.read()

    print("Trying /dev/video" + str(input_port))

    # Wait before trying the next USB port
    time.sleep(1)

# Put image width and height on table
h, w, _ = frame.shape
table.putNumber('frame_width', w)
table.putNumber('frame_height', h)

# Run the pipeline on the video stream
while True:

    _, frame = cap.read()

    if frame is None:
        continue

    # Undistort the frame
    #temp = cv2.undistort(frame, config.cameramtx, config.dist, None, config.newcameramtx)
    # TODO Crop the frame using roi
    #frame = temp


    # Process frame
    visionPipeline = RedBlobPipeline() # LemonVisionGripPipeline()
    visionPipeline.process(frame)


    # Retrieve the blobs from the pipeline
    blobs = visionPipeline.find_blobs_output # tuple of KeyPoint objects

    print(str(len(blobs)) + " blobs detected")

    xCentroids = []
    yCentroids = []
    pitchAngles = []
    yawAngles = []

    # Append the centroid of blobs to the output array
    for i in range(len(blobs)):
        x, y = blobs[i].pt
        x= int(x)
        y=int(y)
        xCentroids.append(x)
        yCentroids.append(y)

        cv2.line(frame, (int(x) - config.line_length, int(y)), (x+config.line_length, y), (0, 0, 255), 2)
        cv2.line(frame, (x, y - config.line_length), (x, y+config.line_length), (0, 0, 255), 2)


        pitch_angle, yaw_angle = calculate_coords(w, h, x, y)
        pitchAngles.append(pitch_angle)
        yawAngles.append(yaw_angle)

        print("pitch: " + str(pitch_angle) + "; yaw: " + str(yaw_angle))

    # Publish centroids on NetworkTables
    sd = NetworkTables.getTable('jetson')

    sd.putNumberArray('xCentroids', xCentroids)
    sd.putNumberArray('yCentroids', yCentroids)
    sd.putNumberArray('pitchAngles', pitchAngles)
    sd.putNumberArray('yawAngles', yawAngles)


    cv2.imshow("image", frame)

    # Put test value in NT
    sd.putString('test', 'hello here is a test str value')

    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break
