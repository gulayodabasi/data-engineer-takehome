import boto3
import argparse
from PIL import Image
import logging
import sys
from io import BytesIO


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


def main():
    """
    Provides a convenient way to accept some information at the command line while running the program.

    Returns:
        dictionary: {aws-src-bucket,  aws-dest-bucket, aws-key-id, aws-secret-key}
    """
    # Create parse
    argParser = argparse.ArgumentParser()

    argParser.add_argument("-aki", "--aws_access_key_id", type=str,
                           help="AWS Access Key ID")
    argParser.add_argument("-sak", "--aws_secret_access_key",
                           type=str, help="AWS Secret Access Key")
    argParser.add_argument("-st", "--aws_session_token", type=str,
                           help="AWS Session Token")
    argParser.add_argument("-sbn", "--src-bucket_name", type=str,
                           help="Source Bucket Name")
    argParser.add_argument("-dbn", "--dst-bucket-name", type=str,
                           help="Destination Bucket Name")

    args = argParser.parse_args()

    # return dictionary that contains command line inputs
    return {'aws-access-key-id': args.aws_access_key_id,
            'aws-secret-access-key': args.aws_secret_access_key,
            'aws-session-token': args.aws_session_token,
            'src-bucket-name': args.src_bucket_name,
            'dst-bucket-name': args.dst_bucket_name
            }


def create_session(aws_access_key_id, aws_secret_access_key, aws_session_token):
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
                            aws_secret_access_key=aws_secret_access_key,
                            aws_session_token=aws_session_token)

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

    logger.info('Object copied.')


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
    # get the bucket
    bucket = s3.Bucket(bucket_name)
    objects = []
    # fetch the all objects under the bucket and convert the bytestring
    for obj in bucket.objects.all():
        key = obj.key
        file_byte_string = obj.get()['Body'].read()
        objects.append({'key': key, 'file_byte_string': file_byte_string})

    return objects


def has_transparency(file_byte_string):
    """
    Takes Byte string as an input parameter to convert and check the transparency

    Args:
        file_byte_string (str): File byte String

    Returns:
        boolean: Returns True if the images has transparency, otherwise returns False
    """
    # load image

    img = Image.open(BytesIO(file_byte_string)).convert('RGBA')

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
    input_dict = main()
    logger.info('Script started')

    aws_access_key_id = input_dict['aws-access-key-id']
    aws_secret_access_key = input_dict['aws-secret-access-key']
    aws_session_token = input_dict['aws-session-token']
    src_bucket_name = input_dict['src-bucket-name']
    dst_bucket_name = input_dict['dst-bucket-name']

    # create session
    session = create_session(
        aws_access_key_id, aws_secret_access_key, aws_session_token)

    # get all objects from the bucket
    files_dict_list = get_all_object_from_s3_bucket(
        session=session, bucket_name=src_bucket_name)

    # check the image has transparency
    for f_dict in files_dict_list:
        if has_transparency(f_dict['file_byte_string']) is True:
            # log the file name if it has transparency
            logger.info(f"{f_dict['key']} has transparent pixels")
        else:
            # copy the file to destination bucket if the image has not transparency
            copy_s3(session=session,
                    source_bucket_name=src_bucket_name,
                    source_bucket_key=f_dict['key'],
                    dest_bucket_key=f_dict['key'],
                    dest_bucket_name=dst_bucket_name)

    logger.info('Script completed')
