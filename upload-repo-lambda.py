import boto3
import StringIO
import zipfile

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:240748614592:DeployBlockWebsiteTopic')
    location = {
        "bucketName":'websitebuild.blockroyalty.com',
        "objectKey": 'blockroyaltybuild.zip'
    }
    try:
        job = event.get("CodePipeline.job")

        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if  artifact["name"] == "MyAppBuild":
                     location = artifact["Location"]["s3Location"]

        print "Building website from " + str(location)

        s3 = boto3.resource('s3')

        website_bucket = s3.Bucket('website.blockroyalty.com')
        build_bucket = s3.Bucket(location["bucketName"])

        website_zip = StringIO.StringIO()
        build_bucket.download_fileobj(location["objectKey"], website_zip)

        with zipfile.ZipFile(website_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                website_bucket.upload_fileobj(obj, nm)
                website_bucket.Object(nm).Acl().put(ACL='public-read')

        print "Job done!"
        topic.publish(Subject="Website Deployed", Message="Website deployed successfully!")
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobID=jobID["id"])
    except:
        topic.publish(Subject="Portfolio Deploy Failed", Message="The Website was not updated successfully")
        raise

    return 'Hello from Lambda'
