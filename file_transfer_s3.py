import boto3
import argparse
from PIL import Image
import logging
import sys


def initialize_logger():
    """
    Initialize logger

    Returns:
        Logger: Initialized logger
    """
    # create logger, set log level
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # initialize the format pattern
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    # initialize the handler, set level and format
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    # initialize the file handler that the logs will be saved
    file_handler = logging.FileHandler('logs.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # add initialized handlers
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    return logger


# run the log initializer
logger = initialize_logger()


def main(argv):
    """
    Provides a convenient way to accept some information at the command line while running the program.

    Returns:
        dictionary: {aws-src-bucket,  aws-dest-bucket, aws-key-id, aws-secret-key}
    """
    # Create parse
    argParser = argparse.ArgumentParser()

    argParser.add_argument("aws-src-bucket", type=str, help="Source bucket")
    argParser.add_argument("aws-dest-bucket", type=str, help="Source bucket")
    argParser.add_argument("aws-key-id", type=str, help="Source bucket")
    argParser.add_argument("aws-secret-key", type=str, help="Source bucket")

    argParser.add_argument("-s", "--save-to-directory",
                           help="Directory that the detected images will be saved")

    args = argParser.parse_args()

    # return dictionary that contains command line inputs
    return {'aws-src-bucket': args.aws_src_bucket,
            'aws-dest-bucket': args.aws_dest_bucket,
            'aws-key-id': args.aws_key_id,
            'aws-secret-key': args.aws_secret_key}


def create_session(aws_access_key_id, aws_secret_access_key):
    """
    Create AWS session by using access key and secret key

    Args:
        aws_access_key_id (str): AWS Access Key
        aws_secret_access_key (str): AWS Secret Access Key

    Returns:
        Session: AWS session
    """
    # create session
    session = boto3.Session(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
    logger.info('Session was created')

    return session


def copy_s3(session, source_bucket_name, source_bucket_key, dest_bucket_name, dest_bucket_key):
    """
    Copy the image from source bucket to target bucket

    Args:
        session (Session): _description_
        source_bucket_name (str): Source Bucket Name
        source_bucket_key (str): Source Bucket Key
        dest_bucket_name (str): Destination Bucket Name
        dest_bucket_key (str): Destination Bucket Key
    """
    s3 = session.resource('s3')

    copy_source = {
        'Bucket': source_bucket_name,
        'Key': source_bucket_key
    }
    bucket = s3.Bucket(dest_bucket_name)
    bucket.copy(copy_source, dest_bucket_key)


def get_all_object_from_s3_bucket(session, bucket_name):
    """
    Get all objects from S3

    Args:
        session (Session): AWS Session
        bucket_name (str): Bucket Name

    Returns:
        _type_: _description_
    """
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    return [item.key for item in bucket.objects]


def has_transparency(file):
    """

    Args:
        file (str): File path

    Returns:
        boolean: Returns True if the images has transparency, otherwise returns False
    """
    # load image
    img = Image.open(file).convert('RGBA')

    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False


# Execute code when the file runs as a script
if __name__ == "__main__":
    aws_access_key_id = 'test'
    aws_secret_access_key = 'test1'
    bucket_name = 'bucket'
    dest_bucket_key = 'dest_bucket_key'
    dest_bucket_name = 'dest_bucket_name'

    # create session
    session = create_session(aws_access_key_id, aws_secret_access_key)
    # get all objects from the bucket
    files = get_all_object_from_s3_bucket(
        session=session, bucket_name=bucket_name)
    # check the image has transparency
    for f in files:
        if has_transparency is True:
            # log the file name if it has transparency
            logger.info(f'{f} has transparent pixels')
        else:
            # copy the file to destination bucket if the image has not transparency
            copy_s3(session=session, source_bucket_name=bucket_name, source_bucket_key=f,
                    dest_bucket_key=f, dest_bucket_name=dest_bucket_name)