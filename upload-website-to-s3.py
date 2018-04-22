import boto3
from botocore.client import config
import StringIO
import zipfile
import minetypes

s3 = boto3.resource('s3', config=Cofig(signature_version='s3v4'))

website_bucket = s3.Bucket('website.blockroyalty.com')
build_bucket = s3.Bucket('websitebuild.blockroyalty.com')

website_zip = StringIO.StringIO()
build_bucket.download_fileobj('blockroyaltybuild.zip', blockroyaltybuild.zip)

with zipfile.ZipFile(blockroyaltybuild.zip) as myzip
      for nm in myzip.namelist():
          obj = myzip.open(nm)
          website_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': minetypes.guess_type(nm)[0]})
          website_bucket.Object(nm).Acl().put(ACL='public-read')
