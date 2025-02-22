# Data Engineer Takehome Test
Please clone this repo in your account, send us the link of the solution in your GitHub account together with your application.

## Problem 1:
Build a Python script that detects faces in an image using OpenCV, and saves the headshots of the detected faces to a specified directory. The script should take as input a file path to an image, a directory path to save the headshots, and output the number of faces detected in the image.
Instructions:
- Use OpenCV's Haar Cascade classifier for face detection
- The script should be written in Python and use the following libraries: OpenCV, Numpy, and PIL (Python Imaging Library)
- The script should be well commented and easy to understand
- The script should be able to handle a variety of image types (e.g. jpeg, png, etc.)
- The script should be able to handle images with multiple faces
- The script should save the headshots in the specified directory with the file name in the format "face_1.jpg", "face_2.jpg", etc.

## Required Packages:
pip install opencv-python <br/>
pip install numpy <br/>
pip install Pillow <br/>

## How to run script:
python3 face-detection.py -h <br/>
python3 face-detection.py -i ./sample_images/multi-ethnicities-various-people-face-portraits_53876-7917.png <br/>
python3 face-detection.py -i /Users/gulayodabasi/PycharmProjects/data-engineer-takehome/sample_images/collage-of-25-mens-portraits-J0TR20.jpg -s detected-faces <br/>

## Reference links
https://docs.opencv.org/3.4/d2/d99/tutorial_js_face_detection.html <br/>
https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html <br/>
https://medium.com/analytics-vidhya/the-ultimate-handbook-for-opencv-pillow-72b7eff77cd7 <br/>
https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format <br/>
https://www.tutorialspoint.com/python/python_command_line_arguments.htm <br/>


## Problem 2: 
Move all image files from one S3 bucket to another S3 bucket, but only if the image has no transparent pixels.

Objective: Write a Python script that uses the Boto3 library to accomplish the following:

- List all the image files in a given S3 bucket
- Check if each image file has transparent pixels
- If an image file has no transparent pixels, copy it to a different S3 bucket
- If an image file has transparent pixels, log it in a separate file

Guidelines:
- Your script should take the name of the source and destination buckets as input
- You should use the Boto3 library to interact with S3
- You should use the Pillow library to check for transparent pixels in an image
- Your script should handle any errors that may occur during the opening of image file, copy process and anywhere else you deem necessary
- Your script should be well commented and easy to understand
- Your script should be executed from the command line

## Required Packages:
pip install Pillow <br/>
pip install boto3 <br/>


## install AWS CLI and get token, access key id and session token
aws sts get-session-token --duration-seconds 900 --serial-number < MFA Device ID >  --token-code < MFA code >

## How to run script:
python3 aws_file_transfer_transparency.py -h <br/>
python3 aws_file_transfer_transparency.py \ <br/>
  -aki <access_key_id>\ <br/>
  -sak <security_access_key>\ <br/>
  -st <session_token>\ <br/>
  -sbn <src_bucket_name>\ <br/>
  -dbn <dst_bucket_name> <br/>

## Reference links
https://stackoverflow.com/questions/65615059/check-if-an-image-is-transparent-or-not
https://dev.to/aws-builders/how-to-list-contents-of-s3-bucket-using-boto3-python-47mm
https://stackoverflow.com/questions/47468148/how-to-copy-s3-object-from-one-bucket-to-another-using-python-boto3