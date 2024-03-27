#!/usr/bin/env python3
"""Inserts a document i python."""


def insert_school(mongo_collection, **kwargs):
    """ Insert the document into the collection"""
    res = mongo_collection.insert_one(kwargs)
    """ Return the inserted document's _id"""
    return res.inserted_id
