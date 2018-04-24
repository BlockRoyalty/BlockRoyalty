import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:240748614592:DeployBlockWebsiteTopic')

    try:
        s3 = boto3.resource('s3')

        website_bucket = s3.Bucket('website.blockroyalty.com')
        build_bucket = s3.Bucket('websitebuild.blockroyalty.com')

        website_zip = StringIO.StringIO()
        build_bucket.download_fileobj('blockroyaltybuild.zip', website_zip)

        with zipfile.ZipFile(website_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                website_bucket.upload_fileobj(obj, nm,
                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                website_bucket.Object(nm).Acl().put(ACL='public-read')

        print "Job done!"
        topic.publish(Subject="Website Deployed", Message="Website deployed successfully!")
    except:
        topic.publish(Subject="Portfolio Deploy Failed", Message="The Website was not updated successfully")
        raise

    return 'Hello from Lambda' 
