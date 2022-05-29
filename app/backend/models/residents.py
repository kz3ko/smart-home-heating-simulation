from dataclasses import fields

from config.config import RESIDENTS_CONFIG
from models.person import Person
from models.house import House
from models.datetime import Datetime


class Residents:

    def __init__(self, house: House, _datetime: Datetime):
        self.config = RESIDENTS_CONFIG
        self.datetime = _datetime
        self.house = house
        self.people = self.__get_people_from_config()

    def __repr__(self):
        return ', '.join([person.name for person in self.people])

    def __iter__(self):
        for person in self.people:
            yield person

    def __get_people_from_config(self) -> list[Person]:
        people = []
        person_field_names = [field.name for field in fields(Person)]
        for person_config in self.config:
            valid_person_config = {
                field: person_config[field] for field in person_config if field in person_field_names
            }
            try:
                person = Person(datetime=self.datetime, house=self.house, **valid_person_config)
            except KeyError:
                raise KeyError(f'There is no mandatory parameter for one of the people in config!')

            people.append(person)

        return people
