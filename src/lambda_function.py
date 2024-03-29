"""
Lambda handler will receive the following event JSON (use for test cases):
{
    "serialNumber": "GXXXXXXXXXXXXXXXXX",
    "batteryVoltage": "xxmV",
    "clickType": "SINGLE" | "DOUBLE" | "LONG"
}
Actions configured for the following:
SINGLE = Run house fan for 60 minutes
Double = Force nest temperature to 72
Long = Text message about empty garage fridge
"""

import boto3
import json
import logging
import urllib3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    
    # Log the incoming JSON event   
    logger.info('Received event: ' + json.dumps(event))
    
    # Extract click type
    event_type=event['clickType']
    
    # Click type is Long, send text message
    if event_type == 'LONG':
        
        # Initialize the SNS client
        sns = boto3.client('sns')
        
        # Set the text message to send
        my_message = 'We are out of juice boxes please put them on the list!'
        
        # Send the slightly annoying text message
        response = sns.publish(
            TopicArn='arn:aws:sns:us-west-2:612471423895:garage-fridge-text',    
            Message=my_message,    
        )
        logger.info('Message sent: ' + my_message)
        
    # Click is single or double, run webhooks for Nest
    else:   
        
        # Get the Maker API Key from Parameter Store so we don't keep it in plain text
        ssm = boto3.client('ssm')
        parameter = ssm.get_parameter(Name='/maker/apikey', WithDecryption=True)
        maker_key=parameter['Parameter']['Value']
        
        # Construct and log the event type
        maker_event = '%s-%s' % (event['serialNumber'], event['clickType'])
        logger.info('Maker event: ' + maker_event)
        
        # Construct and log the webhook URL
        url = 'https://maker.ifttt.com/trigger/%s/with/key/%s' % (maker_event, maker_key)
        logger.info('URL: ' + url)
        
        # Consume the webhook URL
        http = urllib3.PoolManager()
        foo = http.request('POST', url)
        maker_response = foo.data
        
        # Log response from Maker
        logger.info('Response from maker: ' + maker_response.decode())
