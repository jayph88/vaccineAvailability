import boto3
import logging

SNS_ARN = "arn:aws:sns:ap-south-1:968491765901:vaccine_email"
logger = logging.getLogger("CoWin")


class NotifyEmail:
    def __init__(self):
        self.client = boto3.client('sns', region_name='ap-south-1')

    def send(self, **kwargs):
        center = kwargs["center"]
        pin = kwargs["pin"]
        date = kwargs["date"]
        availability = kwargs["availability"]
        address = kwargs["address"]

        subject = f"voila!!! vaccines are available at {center} {pin}"
        body = f"date         : {date}\n" \
               f"availability : {availability}\n" \
               f"center       : {center}\n" \
               f"address      : {address}\n " \
               # f"pin: {pin}\n "

        logger.info("sending email")
        logger.info(f"subject: {subject}")
        logger.info(f"body: {body}")
        try:
            response = self.client.publish(
                TargetArn=SNS_ARN,
                Message=body,
                Subject=subject,
            )
            logger.info("sns publish response: " + str(response))
        except Exception as e:
            logger.exception("Exception occurred while sending notification")