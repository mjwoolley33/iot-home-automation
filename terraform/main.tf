resource "aws_ssm_parameter" "foo" {
  name  = "/maker/apikey"
  type  = "String"
  value = "XXXXXXXXXXXXXX"
}

resource "aws_sns_topic" "garage-fridge-text" {
  name = "garage-fridge-text"
}

resource "aws_sns_topic_subscription" "sms-target" {
  topic_arn = "arn:aws:sns:us-west-2:612471423895:garage-fridge-text"
  protocol  = "sms"
  endpoint  = "+1-111-111-1111"
}

resource "aws_iam_role_policy" "iot-button-policy" {
  name = "iot-button-policy"
  role = "${aws_iam_role.test_role.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
         "sns:Publish",
         "ssm:GetParameter",
         "logs:CreateLogStream",
         "logs:PutLogEvents"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role" "iot-button-role" {
  name = "iot-button-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}