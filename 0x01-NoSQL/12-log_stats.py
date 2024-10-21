#!/usr/bin/env python3
"""
12-log_stats: Script that provides stats about Nginx logs in MongoDB
"""

from pymongo import MongoClient

def log_stats():
    """ Function to gather statistics from the nginx logs """

    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Count the total number of logs
    total_logs = collection.count_documents({})

    # Count the number of logs for each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        method_counts[method] = collection.count_documents({"method": method})

    # Count the number of logs where method=GET and path=/status
    status_check = collection.count_documents({"method": "GET", "path": "/status"})

    # Display the results
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_check} status check")

if __name__ == "__main__":
    log_stats()
