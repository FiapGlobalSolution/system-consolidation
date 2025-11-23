import boto3

def send_alert(message: str):
    sns = boto3.client("sns")

    sns.publish(
        TopicArn="arn:aws:lambda:us-east-2:440185825667:function:farmtech-alerts-lambda",
        Message=message,
        Subject="ALERTA CRÍTICO - Sistema Agrícola"
    )
