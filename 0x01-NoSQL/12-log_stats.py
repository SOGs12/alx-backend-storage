#!/usr/bin/env python
"""Script to generate stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient

def get_log_stats():
    # Connect to MongoDB
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    # Get total number of logs
    total_logs = collection.count_documents({})

    # Get count of each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents({"method": method}) for method in methods}

    # Get count of status check with method=GET and path=/status
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})

    # Display statistics
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    get_log_stats()
