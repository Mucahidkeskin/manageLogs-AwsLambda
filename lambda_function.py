import json
import boto3
from botocore.client import Config
import dateutil.tz

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
            response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': "logbucket71500-staging",
                                                            'Key': object_summary.key},
                                                    ExpiresIn=3600)
            name = object_summary.key
            name = name[(name.rfind("/")+1):]
            date = object_summary.last_modified
            dtimestamp = round(date.timestamp())
            x = {
                "fileName":name,
                "url":response,
                "date":dtimestamp
            }
            if(".json" in x["fileName"]):
                x["fileName"] = x["fileName"].replace(".json","")
                fileList.append(x)
        return fileList
    elif (ev ==  "/getUploadLink"):
        fileName =event["queryStringParameters"]["fileName"]
        userName =event["queryStringParameters"]["name"]
        if((".zip" not in fileName) and (".libatlog" not in fileName)):
            return {status:"400"}
        
        uploadURL=s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': "logbucket71500-staging",
                                                            'Key': userName+"/"+fileName},
                                                    ExpiresIn=2500)
        return uploadURL
    elif (ev ==  "/deleteLog"):
        s3.Object('logbucket71500-staging', event["queryStringParameters"]["name"]).delete()
        s3.Object('logbucket71500-staging', event["queryStringParameters"]["name"].replace(".json",".libatlog")).delete()
        return event["queryStringParameters"]["name"]

    return "no reponse"
    
