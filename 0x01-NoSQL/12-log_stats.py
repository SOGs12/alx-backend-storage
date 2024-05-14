#!/usr/bin/env python3
"""
Script to provide stats about Nginx logs stored in MongoDB.
"""

import pymongo

def main():
    # Connect to MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.logs
    collection = db.nginx

    # Count total logs
    total_logs = collection.count_documents({})

    # Count method types
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents({"method": method}) for method in methods}

    # Count status check
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})

    # Display stats
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"    method {method}: {count}")
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    main()
