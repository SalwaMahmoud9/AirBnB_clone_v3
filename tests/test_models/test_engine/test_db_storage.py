#!/usr/bin/python3
""" TestDBStorage"""
import os
import unittest
import MySQLdb
from models.city import City
from models.state import State
from models.user import User
from models import storage
from datetime import datetime


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 'db_storage test not supported')
class TestDBStorage(unittest.TestCase):
    """TestDBStorage"""

    def test_insert_and_update(self):
        """TestDBStorage"""
        db = MySQLdb.connect(port=3306,
                             user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             db=os.getenv('HBNB_MYSQL_DB'))
        new_user = User(**{'first_name': 'admin',
                           'last_name': 'test',
                           'email': 'admin@test.com',
                           'password': 123})
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        R_oldcount = cur.fetchall()
        cur.close()
        db.close()
        new_user.save()
        db = MySQLdb.connect(port=3306,
                             user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             db=os.getenv('HBNB_MYSQL_DB'))
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        R_newcount = cur.fetchall()
        self.assertEqual(R_newcount[0][0], R_oldcount[0][0] + 1)
        cur.close()
        db.close()

    def test_insert(self):
        """TestDBStorage"""
        new = User(email='test@gmail.com',
                   password='123',
                   first_name='test',
                   last_name='test')

        self.assertFalse(new in storage.all().values())
        new.save()
        self.assertTrue(new in storage.all().values())
        db = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('test@gmail.com', result)
        self.assertIn('123', result)
        self.assertIn('test', result)
        self.assertIn('test', result)
        cursor.close()
        db.close()

    def test_update(self):
        """textDBStorage"""
        new = User(email='test@gmail.com',
                   password='12311',
                   first_name='test',
                   last_name='test')

        db = MySQLdb.connect(port=3306,
                             user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             db=os.getenv('HBNB_MYSQL_DB'))
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) FROM users;')
        old_cnt = cursor.fetchone()[0]
        self.assertTrue(result is None)
        self.assertFalse(new in storage.all().values())
        new.save()
        db1 = MySQLdb.connect(port=3306,
                              user=os.getenv('HBNB_MYSQL_USER'),
                              host=os.getenv('HBNB_MYSQL_HOST'),
                              passwd=os.getenv('HBNB_MYSQL_PWD'),
                              db=os.getenv('HBNB_MYSQL_DB'))
        cursor1 = db1.cursor()
        cursor1.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor1.fetchone()
        cursor1.execute('SELECT COUNT(*) FROM users;')
        new_cnt = cursor1.fetchone()[0]
        self.assertFalse(result is None)
        self.assertEqual(old_cnt + 1, new_cnt)
        self.assertTrue(new in storage.all().values())
        cursor1.close()
        db1.close()
        cursor.close()
        db.close()

    def test_delete(self):
        """TestDBStorage"""
        new = User(email='test@gmail.com',
                   password='12311',
                   first_name='test',
                   last_name='test')

        obj_key = 'User.{}'.format(new.id)
        db = MySQLdb.connect(port=3306,
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             user=os.getenv('HBNB_MYSQL_USER'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             db=os.getenv('HBNB_MYSQL_DB'))
        new.save()
        self.assertTrue(new in storage.all().values())
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('test@gmail.com', result)
        self.assertIn('12311', result)
        self.assertIn('test', result)
        self.assertIn('test', result)
        self.assertIn(obj_key, storage.all(User).keys())
        new.delete()
        self.assertNotIn(obj_key, storage.all(User).keys())
        cursor.close()
        db.close()

    def test_refresh(self):
        """TestDBStorage"""
        db = MySQLdb.connect(port=3306,
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             user=os.getenv('HBNB_MYSQL_USER'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             db=os.getenv('HBNB_MYSQL_DB'))
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO users(id, created_at, updated_at, email, password' +
            ', first_name, last_name) VALUES(%s, %s, %s, %s, %s, %s, %s);',
            [
                '5558-l5m5-7v22c',
                str(datetime.now()),
                str(datetime.now()),
                'test@new.com',
                '147',
                'test',
                'new',
            ]
        )
        self.assertNotIn('User.5558-l5m5-7v22c', storage.all())
        db.commit()

        storage.reload()
        self.assertIn('User.5558-l5m5-7v22c', storage.all())
        cursor.close()
        db.close()

    def test_count(self):
        """ test_count """
        dic = {"name": "Vecindad"}
        state = State(**dic)
        storage.new(state)
        dic = {"name": "Mexico", "state_id": state.id}
        city = City(**dic)
        storage.new(city)
        storage.save()
        c = storage.count()
        self.assertEqual(len(storage.all()), c)
