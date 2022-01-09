from dataclasses import fields

from config.config import RESIDENTS_CONFIG
from models.person import Person


class Residents:

    def __init__(self):
        self.config = RESIDENTS_CONFIG
        self.people = self.__get_people_from_config()

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
                person = Person(**valid_person_config)
            except KeyError:
                raise KeyError(f'There is no mandatory parameter for one of the people in config!')

            people.append(person)

        return people
