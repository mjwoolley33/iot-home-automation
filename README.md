### AWS IOT Button Home Automation

I have automated several common tasks around my house using an AWS IOT button integrated with AWS SNS and the IFTTT platform.  

When the button is pressed the AWS IOT service integrates with a Lambda function to either trigger an IFTTT applet or AWS SNS topic.

IFTTT runs using applets triggered by web requests, you can find a good tutorial here:  https://help.ifttt.com/hc/en-us/articles/360021401373-Creating-your-own-Applet

## Requirements
* 1 AWS IOT Button:  https://www.amazon.com/All-New-AWS-IoT-Enterprise-Button/dp/B075FPHHGG/ref=sr_1_1?keywords=iot+button&qid=1572918412&s=amazon-devices&sr=1-1
* A free-tier AWS account

## Supported Features
##### Single Click
Trigger IFTTT applet to set Nest house fan to run for 15 minutes
##### Double Click
Trigger IFTTT applet to set Nest temperature to 72 degrees
##### Long Click
Send an SMS via AWS SNS to remind me to add drinks to the grocery list

## Lambda Function basics (/src/lambda_function.py)
The lambda event handler will receive an incoming JSON request that uses the following structure:
```
{
    "serialNumber": "GXXXXXXXXXXXXXXXXX",
    "batteryVoltage": "xxmV",
    "clickType": "SINGLE" | "DOUBLE" | "LONG"
}
```

The lambda function will capture the click type and route to the correct destination.

Note:  when calling an IFTTT applet you make an HTTP request to a URL for the applet.  The URL contains your Maker API Key which should be considered a secret.  To prevent storing the secret in clear text I stored it in the SSM Parameter Store.

## Lambda Permissions
The lambda function needs the following IAM permissions to run:
```
    "sns:Publish"
    "ssm:GetParameter"
    "logs:CreateLogStream"
    "logs:PutLogEvents"
```

## Testing the Lambda Function
1. Create the fuction through terraform or manually through the AWS Console
2. Open the lambda function in the function designer view
3. Add a new test event "Single" with the following JSON, repeat for "Double" and "Long":
```
{
  "serialNumber": "SERIALNUMBER123",
  "batteryVoltage": "xxmV",
  "clickType": "SINGLE"
}
```
4.  Click Test
5.  Review logger output, a successful run will contain the following from the IFTTT applet (along with additional verbose messages):
```
Response:
"Congratulations! You've fired the SERIALNUMBER123-SINGLE event"
```
