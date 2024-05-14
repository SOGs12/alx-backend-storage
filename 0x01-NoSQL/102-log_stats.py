#!/usr/bin/env python3
"""Log stats - new version"""

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
logs_collection = client.logs.nginx

def count_logs():
    """Count logs"""
    total_logs = logs_collection.count_documents({})
    print(f"{total_logs} logs")

def count_methods():
    """Count methods"""
    methods = logs_collection.aggregate([
        {"$group": {"_id": "$method", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ])
    print("Methods:")
    for method in methods:
        print(f"    method {method['_id']}: {method['count']}")

def count_status():
    """Count status"""
    status = logs_collection.aggregate([
        {"$group": {"_id": "$status_code", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ])
    status_check = sum([s['count'] for s in status if s['_id'] == 200])
    print(f"{status_check} status check")

def top_ips():
    """Top IPs"""
    top_ips = logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    print("IPs:")
    for ip in top_ips:
        print(f"    {ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    count_logs()
    count_methods()
    count_status()
    top_ips()
