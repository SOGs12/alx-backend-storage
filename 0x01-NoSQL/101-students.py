#!/usr/bin/env python
""" creat a collection of all students sorted by average score"""

def top_students(mongo_collection):
    pipeline = [
        {
            '$project': {
                'name': 1,
                'averageScore': {
                    '$avg': '$topics.score'
                }
            }
        },
        {
            '$sort': {
                'averageScore': -1
            }
        }
    ]

    top_students = list(mongo_collection.aggregate(pipeline))

    return top_students
