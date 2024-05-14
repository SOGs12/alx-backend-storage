#!/usr/bin/env python3
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    total_logs = logs_collection.count_documents({})

    # Count the occurrences of each IP and get the top 10
    top_ips = list(logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]))

    print(f"{total_logs} logs")
    
    # Display the top IPs and their counts
    print("IPs:")
    for ip_data in top_ips:
        print(f"    {ip_data['_id']}: {ip_data['count']}")

    # Include the existing statistics for methods and status checks
    # (You can add this part by adapting from the existing script)
