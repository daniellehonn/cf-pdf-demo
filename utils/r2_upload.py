import boto3
from botocore.exceptions import NoCredentialsError
import urllib.parse
import os
import io

# Configuration
ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
REGION_NAME = os.getenv('R2_REGION_NAME')
R2_ENDPOINT = os.getenv('R2_ENDPOINT')

# Create a session with your R2 credentials
session = boto3.session.Session()
s3_client = session.client(
    service_name='s3',
    region_name=REGION_NAME,
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
)

def upload_file_to_r2(file_data, file_name):
    try:
        # Upload the file
        s3_client.upload_fileobj(file_data, BUCKET_NAME, file_name)
        print(f'Successfully uploaded {file_name} to {BUCKET_NAME}/{file_name}')
    except FileNotFoundError:
        print(f'The file {file_name} was not found.')
    except NoCredentialsError:
        print('Credentials not available.')
    except Exception as e:
        print(f'An error occurred: {e}')

def upload_md_to_r2(md_text, file_name):
    markdown_file = io.BytesIO(md_text.encode('utf-8'))  # Convert string to bytes
    # Step 2: Upload the file to R2
    upload_file_to_r2(markdown_file, f'{file_name.replace(' ', '_')}.md')

def delete_file_from_r2(file_name):
    try:
        # Delete the file
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=file_name)
        print(f'Successfully deleted {file_name} from {BUCKET_NAME}')
    except FileNotFoundError:
        print(f'The file {file_name} was not found.')
    except NoCredentialsError:
        print('Credentials not available.')
    except Exception as e:
        print(f'An error occurred: {e}')

