import os
import tempfile

from functools import reduce

import pymongo

from swagger_server.models import Student

db_client = pymongo.MongoClient("mongodb://mongo:27017")
db = db_client['devops']  # Create/retrieve database
student_db = db['students']  # Create/retrieve collection

student_id_counter = 1


def add(student=None):
    global student_id_counter

    res = student_db.find_one({'first_name': student.first_name,
                               'last_name': student.last_name})
    if res:
        return 'already exists', 409

    student.student_id = student_id_counter
    dic = student.to_dict()
    dic['_id'] = student.student_id
    student_db.insert_one(dic)
    student_id_counter += 1
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = student_db.find_one({'_id': int(student_id)})
    if not student:
        return 'not found', 404
    student['student_id'] = student_id
    return student


def delete(student_id=None):
    student = student_db.find_one({'_id': int(student_id)})
    if not student:
        return 'not found', 404
    student_db.delete_one({'_id': int(student_id)})
    return student_id
