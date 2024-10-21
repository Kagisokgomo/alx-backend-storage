#!/usr/bin/env python3
""" 102-log_stats.py """
from pymongo import MongoClient

def log_stats():
    """ Print statistics about the Nginx logs """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Count total logs
    total_logs = collection.count_documents({})

    print(f"{total_logs} logs")

    # Count methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count_method = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count_method}")

    # Count status check (GET method and path /status)
    status_check = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check} status check")

    # Top 10 most frequent IPs
    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    
    top_ips = collection.aggregate(pipeline)
    
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    log_stats()
