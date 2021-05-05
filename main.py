import json
import datetime
import time
import requests
import logging
import argparse

from email_notification import NotifyEmail

URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
logger = logging.getLogger("CoWin")
logger.setLevel(logging.INFO)
c_handler = logging.StreamHandler()
c_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(c_handler)


class CoWin:
    def __init__(self, age, pin_code, date=datetime.datetime.now().strftime('%d-%m-%Y')):
        """

        :param age:  your age
        :param pin_code: pin code as a string, multiple pin code as "411057,411033"
        :param date: date for which you need to check vaccination
        """
        self.age = age
        self.pin_code = pin_code
        self.date = date

    def request_cowin(self, pincode, date):
        data = {"pincode": pincode, "date": date}
        logger.info(f"checking centres on CoWin for {date} with pin {pincode}")
        try:
            _response = requests.get(url=URL, params=data)
            if _response.status_code != 200:
                logger.warning("Error getting data from CoWin" + _response.text)
            logger.info("found centres on CoWin " + _response.text)
            return json.loads(_response.text)["centers"]
        except Exception as e:
            logger.exception("exception occured while fetching data from CoWin")

    def check_availability(self):
        pin_codes = self.pin_code.split(",")  # pin_code="15454,54552"
        pin_codes = [x for x in pin_codes if x]  # remove empty pin code

        # search for date and day after that
        date_1 = datetime.datetime.strptime(self.date, '%d-%m-%Y')
        date_2 = date_1 + datetime.timedelta(days=1)
        vaccination_dates = [self.date, date_2.strftime('%d-%m-%Y')]
        for vaccination_date in vaccination_dates:
            for pin_code in pin_codes:
                centres = self.request_cowin(pin_code, vaccination_date)
                for center in centres:
                    _name = center['name']
                    _center_availability = center["sessions"][0]
                    _availability = _center_availability['available_capacity']
                    _min_age = _center_availability["min_age_limit"]
                    _pincode = center['pincode']
                    _address = center['address']

                    logger.info(f"checking centre {_name} for availability ")

                    if self.age > _min_age:
                        if 0 < _availability:
                            logger.info(f"{_availability} vaccines "
                                        f"available at {_name}, pin {_pincode} "
                                        f"for date {vaccination_date}")
                            found.append(pin_code)
                            # send some notification
                            NotifyEmail().send(center=_name, availability=_availability, pin=_pincode,
                                               date=vaccination_date, address=_address)
                            return pin_code
                        else:
                            logger.debug(f"vaccinations not available at {_name}")


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
            arg_pin = arg_pin.replace(pin_found, "")
            my_vaccine.pin_code = arg_pin
        time.sleep(150)