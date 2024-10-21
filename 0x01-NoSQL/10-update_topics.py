#!/usr/bin/env python3
"""
10-update_topics: Function that updates topics for a school document
"""

def update_topics(mongo_collection, name, topics):
    """
    Updates the topics of a school document based on the school name.

    Args:
        mongo_collection: The PyMongo collection object.
        name: The name of the school to update.
        topics: A list of topics to update in the school document.

    Returns:
        None
    """
    mongo_collection.update_one(
        {"name": name},  # Filter the document where name matches
        {"$set": {"topics": topics}}  # Set the new topics list
    )
