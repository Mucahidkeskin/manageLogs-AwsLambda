import json
import boto3
from botocore.client import Config
def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
    my_bucket = s3.Bucket('logbucket71500-staging')
    fileList=[]
    count=0
    print(event)
    ev=event["rawPath"]
    if ev=="/getLogs":
        print(event["queryStringParameters"]["name"])
        for object_summary in my_bucket.objects.filter(Prefix = (event["queryStringParameters"]["name"])):
            count+=1
            print(object_summary)
            response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': "logbucket71500-staging",
                                                            'Key': object_summary.key},
                                                    ExpiresIn=3600)
            print(response)
            name = object_summary.key
            name = name[(name.rfind("/")+1):]
            x = {
                "fileName":name,
                "url":response
            }
            if(".json" in x["fileName"]):
                fileList.append(x)
        return fileList
    elif (ev ==  "/getUploadLink"):
        uploadURL=s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': "logbucket71500-staging",
                                                            'Key': event["queryStringParameters"]["name"]},
                                                    ExpiresIn=2500)
        return uploadURL
    elif (ev ==  "/deleteLog"):
        s3.Object('logbucket71500-staging', event["queryStringParameters"]["name"]).delete()
        s3.Object('logbucket71500-staging', event["queryStringParameters"]["name"].replace(".json",".libatlog")).delete()
        return event["queryStringParameters"]["name"]

    return "no reponse"
    
