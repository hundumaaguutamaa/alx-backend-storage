#!/usr/bin/env python3
"""Provides stats about Nginx logs stored in MongoDB."""
from pymongo import MongoClient

if __name__ == "__main__":
  """ Connect to mongodb """
  client = MongoClient('mongodb://127.0.0.1:27017')
  db = client['logs']
  collection = db['nginx']

 print(f"{collection.estimated_document_count()} logs")

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        method_counts = collection.count_documents({'method': method})
        print(f"method {method}: {method_counts}")

    check_get = collection.count_documents(
        {'method': 'GET', 'path': "/status"})
    print(f"{check_get} status check")
