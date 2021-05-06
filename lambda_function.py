import json
import logging

from cowin import CoWin

logger = logging.getLogger("CoWin")
logger.setLevel(logging.INFO)
c_handler = logging.StreamHandler()
c_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(c_handler)


def lambda_handler(event, context):
    arg_pin = event["pin"]
    pin_codes = arg_pin.split(",")  # pin_code="15454,54552"
    age = event["age"]

    for pin in pin_codes:
        my_vaccine = CoWin(age, pin)
        my_vaccine.check_availability()

    return {
        'statusCode': 200,
        'body': json.dumps("lambda invoked successfully ")
    }


if __name__ == "__main__":
    events = {"age": 30, "pin": "411057,411001,144033,411011"}
    lambda_handler(events, "dummy")
