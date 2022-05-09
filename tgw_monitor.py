import boto3
import logging 
import os 

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

sts_client = boto3.client('sts')

assume_role_arn = os.environ.get("ASSUME_ROLE_ARN")

def lambda_handler(event, context):
  LOGGER.info(f"Started assumeing role: {assume_role_arn})
  try:
    assumedRole = sts_client.assume_role(
      RoleArn=assume_role_arn,
      RoleSessionName='network_account_assume_role'
    )
    boto3_session_object = boto3.Session(
                                aws_access_key_id=assumedRole['Credentials']['AccessKeyId'],
                                aws_secret_access_key=assumedRole['Credentials']['SecretAccessKey'],
                                aws_session_token=assumedRole['Credentials']['SessionToken']
                                )
    ec2_client= boto3_session_object.client("ec2")
    try:
      response = ec2Client.describe_transit_gateway_attachments(
          Filters=[
              {
                  'Name': 'resource-type',
                  'Values': [
                      'vpc',
                  ]
              }
      )
      for tgw_attachment in response.get("TransitGatewayAttachments"):
          tgw_attachment_list.append(
                  {
                  "account_id": tgw_attachment.get("ResourceOwnerId"), 
                  "vpc_id": tgw_attachment.get("ResourceId"),
                  "region": region
                  }
              )
    except Exception as error:
        LOGGER.error(error)    
  except Exception as error:
    LOGGER.error(f"Failed to assume Role: {assume_role_arn}")
              
           
  
