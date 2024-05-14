#!/usr/bin/env python3
"""A script to get the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """a Python function that returns the list of school
    having a specific topic"""
    docs =  mongo_collection.find({"topics":topic})
    return [doc for doc in docs]
