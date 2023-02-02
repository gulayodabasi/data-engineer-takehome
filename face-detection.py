import cv2
from PIL import Image
import argparse

def main():
    """
    Provides a convenient way to accept some information at the command line while running the program.

    Returns:
        tuple: (file path,  directory)
    """
    # Create parse
    argParser = argparse.ArgumentParser()
    # add argument for image file path, useage -i or --image-file-path
    argParser.add_argument("-i", "--image-file-path",
                           help="Image file path that will be performed face detection")
    # add argument for the directory that detected images will be saved,
    # useage -s or --save-to-directory
    argParser.add_argument("-s", "--save-to-directory",
                           help="Directory that the detected images will be saved")
    # Get the args from command line
    args = argParser.parse_args()

    return args.image_file_path, args.save_to_directory


def get_file_name_with_extension(path):
    """
    Get the file name and extension from full path

    Args:
        path (str): file path

    Returns:
        str: file name with extension
    """
    return path.strip('/').strip('\\').split('/')[-1].split('\\')[-1]


def face_detection(file_path, save_to_directory='detected-faces'):
    """
    Detects the faces in the images

    Args:
        file_path (str): image file path
        save_to_directory (str, optional): the directory that the detected images will be saved,
                                           default directory is 'detected-faces'
    """
    print('Face detection started...')
    # load the pre-trained classifiers from OpenCV
    face_cascade = cv2.CascadeClassifier(
        './cv2/data/haarcascade_frontalface_default.xml')
    # Load image
    img = cv2.imread(file_path)
    # convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 3)
    # draw rectangle that includes faces in the images
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # print out count of the detected faces in the image
    print(f'Found faces : {len(faces)}')

    # get file name with extension
    file_name = get_file_name_with_extension(file_path)

    # convert the images from BGR to RGB so that Pillow can use it
    cv2_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv2_img)
    # if the is no specified directory , then use the default one, otherwise use the specified one
    if save_to_directory == 'detected-faces' or save_to_directory == '' or save_to_directory is None:
        pil_img.save(f"./detected-faces/{file_name}")
    else:
        pil_img.save(f"{save_to_directory}/{file_name}")

    print('Face detection completed...')


# Execute code when the file runs as a script
if __name__ == "__main__":
    # call the argument parse function and assign the arguments from command line
    file_path, save_to_directory = main()
    # call face detection function
    face_detection(file_path, save_to_directory)
