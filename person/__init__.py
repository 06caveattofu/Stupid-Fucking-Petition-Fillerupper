import json

class Person(object):
    def __init__(self, first_name: str, last_name: str, address: dict, phone_number: str, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone_number = phone_number
        self.email = email

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return f"Person({self.first_name}, {self.last_name}, {self.address['full']}, {self.phone_number}, {self.email})"

    def __dict__(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'phone_number': self.phone_number,
            'email': self.email
        }

    def to_json(self):
        return json.dumps(self.__dict__())
