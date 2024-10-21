#!/usr/bin/env python3
"""
8-all: Function that lists all documents in a collection
"""

def list_all(mongo_collection):
    """
    Lists all documents in a collection.

    Args:
        mongo_collection: The PyMongo collection object.

    Returns:
        A list of documents, or an empty list if no documents.
    """
    return list(mongo_collection.find())
