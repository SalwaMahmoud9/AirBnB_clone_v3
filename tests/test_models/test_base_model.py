#!/usr/bin/python3
""" basemodel """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 'basemodel test not supported')
class test_basemodel(unittest.TestCase):
    """ basemodel """

    def __init__(self, *args, **kwargs):
        """ basemodel """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ basemodel """
        pass

    def tearDown(self):
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_basemodel_default(self):
        """ basemodel """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_basemodel_kwargsInt(self):
        """ basemodel """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_basemodel_kwargs(self):
        """ basemodel """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_basemodel_save(self):
        """ basemodel """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_basemodel_string(self):
        """ basemodel """
        i = self.value()
        dictionary = {}
        dictionary.update(i.__dict__)
        if '_sa_instance_state' in dictionary.keys():
            del dictionary['_sa_instance_state']
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         dictionary))

    def test_basemodel_todict(self):
        """ basemodel """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_basemodel_kwargsNone(self):
        """ basemodel """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_basemodel_kwargs1(self):
        """ basemodel """
        n = {'name': 'test'}
        new = self.value(**n)
        self.assertEqual(new.name, n['name'])

    def test_basemodel_id(self):
        """ basemodel """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_basemodel_created(self):
        """ basemodel """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_basemodel_updated(self):
        """ basemodel """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)
