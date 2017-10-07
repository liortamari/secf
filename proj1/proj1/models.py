from mongoengine import *
from settings import DBHOST

connect(host=DBHOST)


class Student(Document):
    name = StringField(max_length=120, required=True)


class Course(Document):
    name = StringField(max_length=120, required=True)
    points = IntField(min_value=1, max_value=5, required=True)


class Enroll(Document):
    student = ReferenceField('Student')
    course = ReferenceField('Course')
    score = IntField(min_value=0, max_value=100)
