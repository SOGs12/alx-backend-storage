#!/usr/bin/env python3
""" A script that that lists all documents in a collection"""

def list_all(mongo_collection):
    """Return an empty list if no document in the collection"""
    docs = []
    for doc in mongo_collection.find():
        if doc:
            docs.append(doc)
    return docs
