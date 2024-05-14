#!/usr/bin/env python3
"""Create a collection of all students sorted by average score."""

def top_students(mongo_collection):
    """
    Create a collection of all students sorted by their average score.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection.

    Returns:
        list: A list of top students sorted by average score.
    """
    if mongo_collection.count_documents({}) == 0:
        print("The collection is empty.")
        return []

    pipeline = [
        {
            '$project': {
                'name': 1,
                'averageScore': {
                    '$avg': '$topics.score'
                }
            }
        },
        {
            '$sort': {
                'averageScore': -1
            }
        }
    ]

    top_students = list(mongo_collection.aggregate(pipeline))
    return top_students

# Check if the script is executed directly
if __name__ == "__main__":
    # Add your test code or execution logic here
    pass
