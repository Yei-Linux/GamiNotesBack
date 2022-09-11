import json

from bson import json_util

from api.services.crud import CrudService
from config.extensions import mongo


class TopicService(CrudService):
    def __init__(self, collection_name):
        super().__init__(collection_name)

    def find_all(self):
        try:
            responses = mongo.db["topics"].aggregate(
                            [
                                {
                                    "$lookup": {
                                        "from": "notes",
                                        "let": {"id": "$_id"},
                                        "pipeline": [
                                            {
                                                "$match": {
                                                    "$expr": {
                                                        "$and": [
                                                            {
                                                                "$eq": ["$topic_id", "$$id"]
                                                            }
                                                        ]
                                                    }
                                                }
                                            },
                                            {
                                                "$group": {
                                                    "_id": 0,
                                                    "count": {
                                                        "$sum": 1
                                                    }
                                                }
                                            }
                                        ],
                                        "as": "notes_counter"
                                    },
                                },
                                {
                                    "$lookup": {
                                        "from": "notes",
                                        "let": {"id": "$_id"},
                                        "pipeline": [
                                            {
                                                "$match": {
                                                    "$expr": {
                                                        "$and": [
                                                            {
                                                                "$eq": ["$is_memorized", True]
                                                            },
                                                            {
                                                                "$eq": ["$topic_id", "$$id"]
                                                            }
                                                        ]
                                                    }
                                                }
                                            },
                                            {
                                                "$group": {
                                                    "_id": 0,
                                                    "count": {
                                                        "$sum": 1
                                                    }
                                                }
                                            }
                                        ],
                                        "as": "notes_memorized_counter"
                                    },
                                },
                                {
                                    "$set": {
                                        "notes_counter": {
                                            "$arrayElemAt": [
                                                "$notes_counter",
                                                0
                                            ]
                                        },
                                        "notes_memorized_counter": {
                                            "$arrayElemAt": [
                                                "$notes_memorized_counter",
                                                0
                                            ]
                                        }
                                    }
                                },
                                {
                                    "$project": {
                                        "_id": 1,
                                        "title": 1,
                                        "description": 1,
                                        "user_id": 1,
                                        "notes": {"$ifNull": ["$notes_counter.count", 0]},
                                        "notes_memorized": {"$ifNull": ["$notes_memorized_counter.count", 0]}
                                    }
                                }
                            ])

            list_responses = list(responses)
            json_list_responses = list(map(lambda document: json.loads(json_util.dumps(document)), list_responses))

            return json_list_responses
        except Exception as e:
            raise Exception("Error in find all: ", e)


TopicServiceImpl = TopicService("topics")
