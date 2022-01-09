from datetime import datetime


class Datetime:

    def __init__(self):
        self.day, self.month, self.year, self.hour, self.minute = self.__get_current_datetime_splitted()
        self.factor_to_change = None
        self.interval = 1  # In minutes for now.

    def __repr__(self):
        return f'{self.hour:02d}:{self.minute:02d} {self.day:02d}.{self.month:02d}.{self.year}'

    def move(self):
        self.__move_minute()
        self.__move_hour()
        self.__move_day()
        self.__move_month()
        self.__move_year()

    def __move_minute(self):
        self.minute += self.interval
        if self.minute >= 60:
            self.minute = 0
            self.factor_to_change = 'hour'
        else:
            self.factor_to_change = None

    def __move_hour(self):
        if self.factor_to_change == 'hour':
            self.hour += 1
            if self.hour >= 24:
                self.hour = 0
                self.factor_to_change = 'day'

    def __move_day(self):
        if self.factor_to_change == 'day':
            self.day += 1
            if self.day >= 31:
                self.day = 1
                self.factor_to_change = 'month'

    def __move_month(self):
        if self.factor_to_change == 'month':
            self.month += 1
            if self.month >= 12:
                self.month = 1
                self.factor_to_change = 'year'

    def __move_year(self):
        if self.factor_to_change == 'year':
            self.year += 1

    @staticmethod
    def __get_current_datetime_splitted() -> [str]:
        return map(int, datetime.now().strftime('%d %m %Y %H %M').split())
