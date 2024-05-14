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

    if 'topics' in mongo_collection.find_one():
        top_students = list(mongo_collection.aggregate(pipeline))
        return top_students
    else:
        print("The 'topics' field is missing in the collection.")
        return []

# Check if the script is executed directly
if __name__ == "__main__":
    # Add your test code or execution logic here
    pass
