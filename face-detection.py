import numpy as np
import cv2
from PIL import Image

import sys
import argparse


def main(argv):
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--image-file-path",
                           help="Image file path that will be performed face detection")
    argParser.add_argument("-s", "--save-to-directory",
                           help="Directory that the detected images will be saved")

    args = argParser.parse_args()

    return args.image_file_path, args.save_to_directory


def get_file_name_with_extension(path):
    return path.strip('/').strip('\\').split('/')[-1].split('\\')[-1]


def face_detection(file_path, save_to_directory='detected-faces'):
    print('Face detection started...')

    face_cascade = cv2.CascadeClassifier(
        './cv2/data/haarcascade_frontalface_default.xml')

    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 3)

    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

    print(f'Found faces : {len(faces)}')

    file_name = get_file_name_with_extension(file_path)

    cv2_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv2_img)
    if save_to_directory == 'detected-faces' or save_to_directory == '':
        pil_img.save(f"./detected-faces/{file_name}")
    else:
        pil_img.save(f"{save_to_directory}/{file_name}")

    print('Face detection completed...')


if __name__ == "__main__":
    file_path, save_to_directory = main(sys.argv[1:])

    face_detection(file_path, save_to_directory)
