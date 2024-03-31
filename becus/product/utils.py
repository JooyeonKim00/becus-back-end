from django.conf import settings
import boto3, uuid

class FileUploadToS3:
    def __init__(self, file):
        self.file = file
    
    def upload(self, type):
        try:
            # variable
            IMAGE_TYPE = "IMAGE"
            FILE_TYPE = "FILE"
            IMAGE_PREFIX = "p_picture/"
            FILE_PREFIX = "p_manual/"
            file_name = ''
            # create s3_client
            s3_client = boto3.client(
                's3',
                aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
                region_name = settings.AWS_REGION
            )
            # check file type
            if(type == IMAGE_TYPE):
                file_name = IMAGE_PREFIX + self.file.name
            elif(type == FILE_TYPE):
                file_name = FILE_PREFIX + self.file.name
            else:
                raise Exception("File type error")
            s3_client.upload_fileobj(self.file, settings.AWS_STORAGE_BUCKET_NAME, file_name)
            return f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{file_name}'
        except:
            return None