import json
import datetime
import requests
import logging

from email_notification import NotifyEmail

URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
logger = logging.getLogger("CoWin")


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
                            # send some notification
                            NotifyEmail().send(center=_name, availability=_availability, pin=_pincode,
                                               date=vaccination_date, address=_address)
                            return pin_code
                        else:
                            logger.info(f"vaccinations not available at {_name}")
