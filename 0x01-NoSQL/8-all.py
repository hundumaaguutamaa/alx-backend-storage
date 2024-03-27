#!/usr/bin/env python3
""" List all document."""

def list_all(mongo_collection):
    """lists all documents in a collection"""
    return [doc for doc in mongo_collection.find()]
