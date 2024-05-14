# Add necessary imports here

# MongoDB connection setup
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['your_database_name']
    collection = db['your_collection_name']
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

# MongoDB aggregation pipeline
pipeline = [
    { '$group': { '_id': '$ip', 'count': { '$sum': 1 } } },
    { '$sort': { 'count': -1 } },
]

# Execute the aggregation query
try:
    result = list(collection.aggregate(pipeline))
    total_logs = len(result)
    top_ips = result[:10]  # Extract top 10 IP addresses
except Exception as e:
    print(f"Error during aggregation: {e}")
    sys.exit(1)

# Output formatting
print(f"Total number of logs: {total_logs}")
print("Top 10 IP addresses with the highest occurrence:")
for idx, ip_data in enumerate(top_ips, start=1):
    print(f"#{idx}: IP Address: {ip_data['_id']}, Count: {ip_data['count']}")

# Additional aggregation for methods and status checks can be added here
