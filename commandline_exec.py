import argparse
import datetime
import time
import logging

from cowin import CoWin

logger = logging.getLogger("CoWin")
logger.setLevel(logging.INFO)
c_handler = logging.StreamHandler()
c_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(c_handler)

if __name__ == "__main__":
    found = list()
    parser = argparse.ArgumentParser(description='search vaccines nearby')
    parser.add_argument('--age', type=int, help='age of the person')
    parser.add_argument('--pin', type=str, help='comma separated pin code in quotes')
    args = parser.parse_args()
    arg_pin = args.pin
    arg_age = args.age
    start_date = datetime.datetime.now()
    my_vaccine = CoWin(arg_age, arg_pin)

    while True:
        todays_date = datetime.datetime.now()
        # reset search parameters on next day
        if start_date.day != todays_date.day:
            start_date = datetime.datetime.now()
            arg_pin = args.pin
            arg_age = args.age
            my_vaccine = CoWin(arg_age, arg_pin)
            found = []

        # search only if pin are available
        if arg_pin != "":
            pin_found = my_vaccine.check_availability()

        # remove searching for a pin for a day if found
        if pin_found:
            found.append(pin_found)
            arg_pin = arg_pin.replace(pin_found, "")
            my_vaccine.pin_code = arg_pin
        time.sleep(150)