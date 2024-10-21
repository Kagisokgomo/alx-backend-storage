#!/usr/bin/env python3
"""
9-insert_school: Function to insert a new document into the collection
"""

def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into the given collection.

    Args:
        mongo_collection: The PyMongo collection object.
        kwargs: The keyword arguments representing the document fields.

    Returns:
        The _id of the new document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
