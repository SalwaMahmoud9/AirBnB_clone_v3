#!/usr/bin/python3
""" test_City """
from tests.test_models.test_base_model import test_basemodel
from models.city import City
import os


class test_City(test_basemodel):
    """ test_City """

    def __init__(self, *args, **kwargs):
        """ test_City """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_City_name(self):
        """ test_City """
        new = self.value()
        self.assertEqual(type(new.name), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_City_state_id(self):
        """ test_City """
        new = self.value()
        self.assertEqual(type(new.state_id), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))
