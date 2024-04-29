#!/usr/bin/python3
"""TestDBStorageWithConsole"""
import json
import os
import MySQLdb
import unittest
from io import StringIO
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 'file_storage test not supported here')
class TestDBStorageWithConsole(unittest.TestCase):
    """TestDBStorageWithConsole"""
    def query(self, string):
        """TestDBStorageWithConsole"""
        db = MySQLdb.connect(port=3306,
                             user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             db=os.getenv('HBNB_MYSQL_DB'))
        cur = db.cursor()
        cur.execute(string)
        count = cur.fetchall()
        cur.close()
        db.close()
        return count

    def test_DBStorage_create_state(self):
        """TestDBStorageWithConsole"""
        string = "SELECT * FROM states"
        old_count = self.query(string)
        cmd = 'create State name="Alexandria"'
        self.getOutput(cmd)
        new_count = self.query(string)
        self.assertEqual(len(new_count) - len(old_count), 1)

    def getOutput(self, command):
        """TestDBStorageWithConsole"""
        with patch('sys.stdout', new=StringIO()) as out:
            cmd = HBNBCommand()
            cmd.onecmd(command)
            return out.getvalue().strip()

    def test_DBStorage_create_place_with_integer_and_float(self):
        """TestDBStorageWithConsole"""
        string = "SELECT * FROM places"
        cmd = 'create State name="Alexandria"'
        state_id = self.getOutput(cmd)
        name = "Alex"
        cmd = f'create City state_id="{state_id}" name="{name}"'
        city_id = self.getOutput(cmd)
        cmd = f'create User email="test@new.com"\
            password="123" first_name="test" last_name="new"'
        user_id = self.getOutput(cmd)
        cmd = f'create Place city_id="{city_id}" user_id="{user_id}"\
            name="home" description="homeDesc" number_rooms=3\
            number_bathrooms=2 max_guest=5 price_by_night=300 latitude=132.22\
            longitude=158.42'
        place_id = self.getOutput(cmd)
        new_count = self.query(string)
        self.assertIn(place_id, str(new_count))
        self.assertIn('100', str(new_count))
        self.assertIn('120.12', str(new_count))

    def test_DBStorage_create_city_with_underscore(self):
        """TestDBStorageWithConsole"""
        string = "SELECT * FROM cities"
        old_count = self.query(string)
        cmd = 'create State name="Alexandria"'
        state_id = self.getOutput(cmd)
        name = "San_Francisco_is_super_cool"
        cmd = f'create City state_id="{state_id}" name="{name}"'
        city_id = self.getOutput(cmd)
        new_count = self.query(string)
        self.assertEqual(len(new_count) - len(old_count), 1)
        cmd = 'show City {}'.format(city_id)
        output = self.getOutput(cmd)
        self.assertIn(name.replace('_', ' '), output)

    def test_DBStorage_create_city_without_underscore(self):
        """TestDBStorageWithConsole"""
        string = "SELECT * FROM cities"
        cmd = 'create State name="Alexandria"'
        state_id = self.getOutput(cmd)
        name = "Fremont"
        cmd = f'create City state_id="{state_id}" name="{name}"'
        self.getOutput(cmd)
        new_count = self.query(string)
        self.assertIn(name.replace('_', ' '), str(new_count))


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 'console test not supported')
class TestHBNBCommand(unittest.TestCase):
    """TestDBStorageWithConsole"""

    def test_DBStorage_consolev001(self):
        from tests import clear_stream
        """TestDBStorageWithConsole"""
        with patch('sys.stdout', new=StringIO()) as c:
            cs = HBNBCommand()
            cs.onecmd('')
            cs.onecmd('    ')
            self.assertEqual(c.getvalue(), '')
            clear_stream(c)
            cs.onecmd('ls')
            cs.onecmd('')
            cs.onecmd('  ')
            self.assertEqual(c.getvalue(), '*** Unknown syntax: ls\n')
            clear_stream(c)
            cs.onecmd('help')
            self.assertNotEqual(c.getvalue().strip(), '')
            clear_stream(c)
            cs.onecmd('help quit')
            self.assertNotEqual(c.getvalue().strip(), '')
            clear_stream(c)
            self.assertTrue(cs.onecmd('EOF'))
            self.assertTrue(cs.onecmd('quit'))

    def test_DBStorage_consolev01(self):
        from tests import clear_stream
        """TestDBStorageWithConsole"""
        with patch('sys.stdout', new=StringIO()) as c:
            cs = HBNBCommand()
            if os.path.isfile('file.json'):
                os.unlink('file.json')
            clear_stream(c)
            cs.onecmd('create')
            self.assertEqual(c.getvalue(), "** class name missing **\n")
            clear_stream(c)
            cs.onecmd('create Base')
            self.assertEqual(c.getvalue(), "** class doesn't exist **\n")
            clear_stream(c)
            cs.onecmd('create base')
            self.assertEqual(c.getvalue(), "** class doesn't exist **\n")
            clear_stream(c)
            cs.onecmd('create BaseModel')
            mdl_sid = 'BaseModel.{}'.format(c.getvalue().strip())
            self.assertTrue(mdl_sid in storage.all().keys())
            self.assertTrue(type(storage.all()[mdl_sid]) is BaseModel)
            with open('file.json', mode='r') as file:
                json_obj = json.load(file)
                self.assertTrue(type(json_obj) is dict)
                self.assertTrue(mdl_sid in json_obj)
            clear_stream(c)
            cs.onecmd('all Base')
            self.assertEqual(c.getvalue(), "** class doesn't exist **\n")
            clear_stream(c)
            cs.onecmd('all base')
            self.assertEqual(c.getvalue(), "** class doesn't exist **\n")
            clear_stream(c)
            cs.onecmd('create BaseModel')
            mdl_id = c.getvalue().strip()
            mdl_sid = 'BaseModel.{}'.format(mdl_id)
            clear_stream(c)
            cs.onecmd('create Amenity')
            mdl_id1 = c.getvalue().strip()
            mdl_sid1 = 'Amenity.{}'.format(mdl_id1)
            self.assertTrue(mdl_sid in storage.all().keys())
            self.assertTrue(mdl_sid1 in storage.all().keys())
            clear_stream(c)
            cs.onecmd('all BaseModel')
            self.assertIn('[BaseModel] ({})'.format(mdl_id), c.getvalue())
            self.assertNotIn('[Amenity] ({})'.format(mdl_id1), c.getvalue())
            clear_stream(c)
            cs.onecmd('all')
            self.assertIn('[BaseModel] ({})'.format(mdl_id), c.getvalue())
            self.assertIn('[Amenity] ({})'.format(mdl_id1), c.getvalue())
            clear_stream(c)
            cs.onecmd('update BaseModel')
            self.assertEqual(c.getvalue(), "** instance id missing **\n")
            clear_stream(c)
            cs.onecmd('update BaseModel 58ebee8b-562e-98c7-821616v66818')
            self.assertEqual(c.getvalue(), "** no instance found **\n")
            clear_stream(c)
            cs.onecmd('create BaseModel')
            mdl_id = c.getvalue().strip()
            clear_stream(c)
            cs.onecmd('update BaseModel {}'.format(mdl_id))
            self.assertEqual(c.getvalue(), "** attribute name missing **\n")
            clear_stream(c)
            cs.onecmd('update BaseModel {} first_name'.format(mdl_id))
            self.assertEqual(c.getvalue(), "** value missing **\n")
            clear_stream(c)
            if os.path.isfile('file.json'):
                os.unlink('file.json')
            self.assertFalse(os.path.isfile('file.json'))
            cs.onecmd('update BaseModel {} first_name Boy'.format(mdl_id))
            self.assertEqual(c.getvalue(), "")
            mdl_sid = 'BaseModel.{}'.format(mdl_id)
            self.assertTrue(mdl_sid in storage.all().keys())
            self.assertTrue(os.path.isfile('file.json'))
            self.assertTrue(hasattr(storage.all()[mdl_sid], 'first_name'))
            self.assertEqual(
                getattr(storage.all()[mdl_sid], 'first_name', ''),
                'Boy'
            )

    def test_DBStorage_user(self):
        """TestDBStorageWithConsole"""
        from tests import clear_stream
        with patch('sys.stdout', new=StringIO()) as c:
            cs = HBNBCommand()
            cs.onecmd('create User')
            mdl_id = c.getvalue().strip()
            clear_stream(c)
            cs.onecmd('show User {}'.format(mdl_id))
            self.assertIn(mdl_id, c.getvalue())
            self.assertIn('[User] ({})'.format(mdl_id), c.getvalue())
            clear_stream(c)
            cs.onecmd('all User')
            self.assertIn(mdl_id, c.getvalue())
            self.assertIn('[User] ({})'.format(mdl_id), c.getvalue())
            clear_stream(c)
            cs.onecmd('update User {} first_name Girl'.format(mdl_id))
            cs.onecmd('show User {}'.format(mdl_id))
            self.assertIn(mdl_id, c.getvalue())
            self.assertIn(
                "'first_name': 'Girl'".format(mdl_id),
                c.getvalue()
            )
            clear_stream(c)
            cs.onecmd('destroy User {}'.format(mdl_id))
            self.assertEqual(c.getvalue(), '')
            cs.onecmd('show User {}'.format(mdl_id))
            self.assertEqual(c.getvalue(), '** no instance found **\n')

    def test_DBStorage_state(self):
        """TestDBStorageWithConsole"""
        from tests import clear_stream
        with patch('sys.stdout', new=StringIO()) as c:
            cs = HBNBCommand()
            clear_stream(c)
            cs.onecmd('create State name="Alexandria"')
            mdl_id = c.getvalue().strip()
            clear_stream(c)
            cs.onecmd('show State {}'.format(mdl_id))
            self.assertIn(mdl_id, c.getvalue())

    def test_DBStorage_classAll(self):
        from tests import clear_stream
        """test_class_all"""
        with patch('sys.stdout', new=StringIO()) as c:
            cs = HBNBCommand()
            cs.onecmd('create City')
            mdl_id = c.getvalue().strip()
            clear_stream(c)
            cmd_line = cs.precmd('City.all()'.format(mdl_id))
            cs.onecmd(cmd_line)
            self.assertIn(mdl_id, c.getvalue())

    def test_DBStorage_classShow(self):
        from tests import clear_stream
        """TestDBStorageWithConsole"""
        with patch('sys.stdout', new=StringIO()) as c:
            cs = HBNBCommand()
            cs.onecmd('create City')
            mdl_id = c.getvalue().strip()
            clear_stream(c)
            cmd_line = cs.precmd('City.show({})'.format(mdl_id))
            cs.onecmd(cmd_line)
            self.assertIn(mdl_id, c.getvalue())

    def test_DBStorage_classDestroy(self):
        from tests import clear_stream
        """TestDBStorageWithConsole"""
        with patch('sys.stdout', new=StringIO()) as c:
            cs = HBNBCommand()
            cs.onecmd('create City')
            mdl_id = c.getvalue().strip()
            clear_stream(c)
            cmd_line = cs.precmd('City.destroy({})'.format(mdl_id))
            cs.onecmd(cmd_line)
            clear_stream(c)
            cs.onecmd('show City {}'.format(mdl_id))
            self.assertEqual(c.getvalue(), "** no instance found **\n")

    def test_DBStorage_create_kwargsfsv(self):
        from tests import clear_stream
        """TestDBStorageWithConsole"""
        with patch('sys.stdout', new=StringIO()) as c:
            cs = HBNBCommand()
            cs.onecmd('create User email="test@email.com" password=123' +
                      ' first_name="new"')
            user_id = c.getvalue().strip()
            clear_stream(c)
            cs.onecmd('show User ' + user_id)
            user_info = c.getvalue().strip()
            self.assertIn("'first_name': 'new'", user_info)
            self.assertIn("'email': 'test@email.com'", user_info)
            if os.getenv('HBNB_TYPE_STORAGE') == 'db':
                self.assertIn("'password': '123'", user_info)
            else:
                self.assertIn("'password': 123", user_info)
            clear_stream(c)

    def test_DBStorage_class_update11(self):
        from tests import clear_stream
        """TestDBStorageWithConsole"""
        with patch('sys.stdout', new=StringIO()) as c:
            cs = HBNBCommand()
            cs.onecmd('create Amenity')
            mdl_id = c.getvalue().strip()
            clear_stream(c)
            cmd_line = cs.precmd(
                'Amenity.update({}, '.format(mdl_id) +
                "{'name': 'Football'})"
            )
            cs.onecmd(cmd_line)
            cs.onecmd('show Amenity {}'.format(mdl_id))
            self.assertIn(
                "'name': 'Football'",
                c.getvalue()
            )

    def test_DBStorage_class_update00(self):
        from tests import clear_stream
        """TestDBStorageWithConsole"""
        with patch('sys.stdout', new=StringIO()) as c:
            cs = HBNBCommand()
            cs.onecmd('create Place')
            mdl_id = c.getvalue().strip()
            clear_stream(c)
            cmd_line = cs.precmd(
                'Place.update({}, '.format(mdl_id) +
                'name, "Cairo")'
            )
            cs.onecmd(cmd_line)
            cs.onecmd('show Place {}'.format(mdl_id))
            self.assertIn(
                "'name': 'Cairo'",
                c.getvalue()
            )
