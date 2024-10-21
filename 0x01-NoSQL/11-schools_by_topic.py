#!/usr/bin/env python3
"""
11-schools_by_topic: Function that returns schools with a specific topic
"""

def schools_by_topic(mongo_collection, topic):
    """
    Finds and returns all schools that have a specific topic in their 'topics' field.

    Args:
        mongo_collection: The PyMongo collection object.
        topic (str): The topic to search for.

    Returns:
        list: A list of schools that contain the topic in their topics list.
    """
    return list(mongo_collection.find({"topics": topic}))
