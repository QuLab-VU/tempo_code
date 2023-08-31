# Wasabi Data Upload/Download
The `wasabi_data_transfer.ipynb` provides examples for how to upload and download files from 
Wasabi S3 buckets using python and Boto3.

## Using AWS Command Line Tools

### Downloading the contents of a Wasabi bucket
1. Install the AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

2. Configure AWS credentials using access keys:
```
$ aws configure
AWS Access Key ID [None]: YOUR_ACCCESS KEY_ID
AWS Secret Access Key [None]: YOUR_SECRET_KEY
Default region name [None]: us-east-2
Default output format [None]: json
```

3. Use `cp` command to download the contents of the bucket:
```
$ aws s3 cp s3://bucket-name DESTINATION --recursive --endpoint-url=https://s3.us-east-2.wasabisys.com
```
Substitute the DESTINATION placeholder with the location of where you want the data downloaded.
