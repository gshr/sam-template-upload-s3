import uuid
import os
import boto3
import uvicorn
from fastapi import FastAPI, File, UploadFile
from mangum import Mangum
import datetime

app = FastAPI()

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
BUCKET_NAME = os.environ['AWS_BUCKET_NAME']
TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)


@app.post('/upload')
def upload_image(file: UploadFile = File(...)):
    id = str(uuid.uuid4())
    filename = f"{id}{file.filename}"
    s3.upload_fileobj(file.file, BUCKET_NAME, filename)

    table.put_item(Item={
        'id': id,
        'create_date': str(datetime.datetime.now()),
        'filename': filename

    })

    response = {
        "statusCode": 200,
        "body": {
            "message": "Upload successfully"
        }
    }

    return response


handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app)
