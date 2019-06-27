# Practicum I - Customer Counter
# Regis University
# Josh Butch

# This file modified from the original file located at: https://www.pyimagesearch.com/2018/08/13/opencv-people-counter/

# This file is the people counter used to count the customers entering and exiting
# the store.  The yellow line of demarcation marks the threshold to the grocery area.

# Import the necessary packages
from pyimagesearch.centroidtracker import CentroidTracker
from pyimagesearch.trackableobject import TrackableObject
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2

# Construct and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-i", "--input", type=str,
	help="path to optional input video file")
ap.add_argument("-o", "--output", type=str,
	help="path to optional output video file")
ap.add_argument("-c", "--confidence", type=float, default=0.4,
	help="minimum probability to filter weak detections")
ap.add_argument("-s", "--skip-frames", type=int, default=30,
	help="# of skip frames between detections")
args = vars(ap.parse_args())

# Initialize the list of class labels MobileNet SSD was trained to
# detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

# Load the serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# If a video path was not supplied, reference the webcam
if not args.get("input", False):
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()          # src=0 is the webcam
	time.sleep(2.0)

# Otherwise, grab a reference to the video file being inputted
else:
	print("[INFO] opening video file...")
	vs = cv2.VideoCapture(args["input"])

# Initialize the video writer if needed
writer = None

# Initialize the frame dimensions or set them from the first frame of video
W = None
H = None

# Instantiate our centroid tracker 
ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
trackers = []           # Initialize a list to store each of our dlib correlation trackers
trackableObjects = {}   # Intialize a dictionary to map each unique object ID to a TrackableObject

# Initialize the total number of frames processed  
totalFrames = 0
totalDown = 0    # Total # of objects down
totalUp = 0      # Total # of objects up

# Start the frames per second throughput estimator
fps = FPS().start()

# Loop over frames from vs
while True:
	# Capture the next frame and determine either VideoCapture or VideoStream
	frame = vs.read()
	frame = frame[1] if args.get("input", False) else frame

	# If we are viewing a video and there's no frame to grab we've reached the end
	if args["input"] is not None and frame is None:
		break

	# Resize the frame to have a maximum width of 500 pixels 
	frame = imutils.resize(frame, width=500)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the frame from BGR to RGB for dlib

	# If the frame dimensions are empty, set them according to shape
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	# Initialize the writer if necessary
	if args["output"] is not None and writer is None:
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 30,
			(W, H), True)

	# Initialize the current status along with our list of bounding
	# box rectangles returned by either (1) our object detector or
	# (2) the correlation trackers
	status = "Waiting"
	rects = []

	# Check to see if we should run a more resource intensive
	# object detection method to help our tracker
	if totalFrames % args["skip_frames"] == 0:
		status = "Detecting"  # Set the status and initialize our new set of object trackers
		trackers = []

		# Convert the frame to a blob and pass the blob through the
		# network and obtain the object detections
		blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
		net.setInput(blob)
		detections = net.forward()

		# loop over the detections
		for i in np.arange(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]     # Extract the probability associated with the detection

			# Filter out weak detections 
			if confidence > args["confidence"]:
				idx = int(detections[0, 0, i, 1])  # Extract the index of the class label from the detections list

				# If the class label is not a person, ignore it
				if CLASSES[idx] != "person":
					continue

				# Compute the coordinates of the bounding box for the object
				box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
				(startX, startY, endX, endY) = box.astype("int")

				 from the bounding
				tracker = dlib.correlation_tracker()  # Construct a dlib rectangle object
				rect = dlib.rectangle(startX, startY, endX, endY)
				tracker.start_track(rgb, rect)        # Start the dlib correlation tracker

				trackers.append(tracker)  # Add to list of trackers

	# Utilize our object *trackers* rather than object *detectors* to obtain a higher frame processing throughput
	else:
		# Loop over the trackers
		for tracker in trackers:
			status = "Tracking"  # Set the status of our system to be 'tracking'

			# Update the tracker and grab the updated position
			tracker.update(rgb)
			pos = tracker.get_position()

			# Unpack the position object
			startX = int(pos.left())
			startY = int(pos.top())
			endX = int(pos.right())
			endY = int(pos.bottom())

			# Add the bounding box coordinates to the rectangles list
			rects.append((startX, startY, endX, endY))

	# Draw a horizontal line in the center of the frame -- once an
	# object crosses this line we will determine whether they were
	# moving 'up' or 'down'
	cv2.line(frame, (0, H // 2), (W, H // 2), (0, 255, 255), 2)

	objects = ct.update(rects)

	# Loop over the tracked objects
	for (objectID, centroid) in objects.items():
		to = trackableObjects.get(objectID, None) # Check to see if a trackable object exists for current object ID

		# If none, create one
		if to is None:
			to = TrackableObject(objectID, centroid)

		else:
			# The difference between the y-coordinate of the *current*
			# centroid and the mean of *previous* centroids will tell
			# us in which direction the object is moving (negative for
			# 'up' and positive for 'down')
			y = [c[1] for c in to.centroids]
			direction = centroid[1] - np.mean(y)
			to.centroids.append(centroid)

			# Check to see if the object has been counted or not
			if not to.counted:
				# If the direction is negative (indicating the object
				# is moving up) AND the centroid is above the center
				# line, count the object
				if direction < 0 and centroid[1] < H // 2:
					totalUp += 1
					to.counted = True

				# If the direction is positive (indicating the object
				# is moving down) AND the centroid is below the
				# center line, count the object
				elif direction > 0 and centroid[1] > H // 2:
					totalDown += 1
					to.counted = True

		# Store the trackable object
		trackableObjects[objectID] = to

		# Draw both the ID of the object and the centroid of the
		# object on the output frame
		text = "ID {}".format(objectID)
		cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

	# Construct a tuple of information to display on the frame
	info = [
		("Up", totalUp),
		("Down", totalDown),
		("Status", status),
	]

	# Loop over the info tuples and draw them on our frame
	for (i, (k, v)) in enumerate(info):
		text = "{}: {}".format(k, v)
		cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
			cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

	# Check to see if we should write the frame to disk
	if writer is not None:
		writer.write(frame)

	# Show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# If the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# Increment the total number of frames processed thus far and
	# then update the FPS counter
	totalFrames += 1
	fps.update()

# Stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# Check to see if we need to release the video writer pointer
if writer is not None:
	writer.release()

# If not using a video file, stop the camera video stream
if not args.get("input", False):
	vs.stop()

# Release the video file pointer
else:
	vs.release()

# Close any open windows
cv2.destroyAllWindows()