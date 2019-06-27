# Practicum I - Still Image Detector
# Regis University
# Josh Butch

#  This file was modified from: https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/

#  This file is the still image object detector, or stage 1 of my final practicum project.

# Import packages
import numpy as np
import argparse     # Package to create argument parser
import time         # Package to track time
import cv2          # OpenCV - package that contains YOLO and dnn module
import os           # Package allows operating system dependent functionality

# Create the argument parser and parse the arguments
ap = argparse.ArgumentParser()                                  # Truncate to ap
ap.add_argument("-i", "--image", required=True,                 # Argument requiring an image to continue
	help="path to input image")                                 # Response to a help query
ap.add_argument("-y", "--yolo", required=True,                  # Argument requiring a path to the YOLO directory
	help="base path to YOLO directory")                         # Response to a help query
ap.add_argument("-c", "--confidence", type=float, default=0.5,  # Argument to adjust confidence interval defaulted to 0.5
	help="minimum probability to filter weak detections")       # Response to help query
ap.add_argument("-t", "--threshold", type=float, default=0.3,   # Argument to adjust non-maxima suppression threshold
	help="threshold when applyong non-maxima suppression")      # Response to help query
args = vars(ap.parse_args())

# Load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([args["yolo"], "coco.names"]) # Define the path to the labels directory
LABELS = open(labelsPath).read().strip().split("\n") # Read the labels, strip any whitespace, and put each one on a new line

# Create a color set for each object in LABELS
np.random.seed(42) # Set the random seed
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8") # Create a list of colors for each object in LABELS

# The paths to the YOLO weights and model configuration files in the yolo-coco directory
weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"]) # Path to the weights file
configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])      # Path to the configuration file

# Load the YOLO object detector trained on the COCO dataset - all 80 classes
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath) # Calling the OpenCV deep neural network (dnn) module based
                                                          # on config and weights files

# Load the input image and record it's spatial dimensions
image = cv2.imread(args["image"])   # Load the image 
(H, W) = image.shape[:2]            # Setting the dimensions as 2 columns - H, W

# Determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Construct a blob from the input image and then perform a forward
# pass of the YOLO object detector, giving us our bounding boxes and
# associated probabilities
blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), # Creating the blob with the dnn package
	swapRB=True, crop=False)                               # swapRB converts a 3-channel BGR image color scheme to RGB
net.setInput(blob)                                         # Sets the new input value for the neural network
start = time.time()                                        # Track start time
layerOutputs = net.forward(ln)                             # Identifies the names of the layers where outputs (blobs) are needed
end = time.time()                                          # Track end time

# Show timing information on YOLO
print("[INFO] YOLO took {:.6f} seconds".format(end - start))

# Initialize the lists of detected bounding boxes, confidences, and
# class IDs.  Brackets ([]) symbolize the list datatype in Python.
boxes = []
confidences = []
classIDs = []

# Loop over each of the layer outputs
for output in layerOutputs:
	# Loop over each of the detections
	for detection in output:
		# Extract the class ID and confidence (i.e., probability) of the current object detection
		scores = detection[5:]
		classID = np.argmax(scores)
		confidence = scores[classID]

		# Filter out weak predictions by ensuring the detected probability is greater than the minimum probability
		if confidence > args["confidence"]:
			# Scale the bounding box coordinates to the size of the image, keeping in mind that YOLO actually
			# returns the center (x, y)-coordinates of the bounding box followed by the boxes' width and height
			box = detection[0:4] * np.array([W, H, W, H])
			(centerX, centerY, width, height) = box.astype("int")

			# Use the center (x, y)-coordinates to derive the top and
			# and left corner of the bounding box
			x = int(centerX - (width / 2))  # From the center X coord subract half the width to get left edge
			y = int(centerY - (height / 2)) # From the center Y coord subtract half the height to get top edge

			# Update our list of bounding box coordinates, confidences, and class IDs
			boxes.append([x, y, int(width), int(height)])
			confidences.append(float(confidence))
			classIDs.append(classID)

# Performs non maximum suppression given boxes and corresponding scores
idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
	args["threshold"])

# Ensure at least one detection exists
if len(idxs) > 0:
	# Loop over the indexes we are keeping
	for i in idxs.flatten():
		# Extract the bounding box coordinates
		(x, y) = (boxes[i][0], boxes[i][1]) # X and Y center coords
		(w, h) = (boxes[i][2], boxes[i][3]) # W and H dimensions 

		# Draw a bounding box rectangle and label on the image
		color = [int(c) for c in COLORS[classIDs[i]]]                    # Assigning a color for the bounding box
		cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)           # Rectangle coords based on image, X, Y, H, W
		text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])  # Assigning the data to be displayed on bounding boxes
		cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,   # Assigning font characteristics
			0.5, color, 2)

# Show the output image
cv2.imshow("Image", image)
cv2.waitKey(0) # Waits for a pressed key in milliseconds - in this case it will wait indefinitely