import json
import re

import pymongo
from bson import ObjectId

from api.services.crud import CrudService
from config.extensions import mongo


class TopicService(CrudService):
    def __init__(self,collection_name):
        super().__init__(collection_name)

    def find_all_v1(self, filters_pagination):
        skip = int(filters_pagination["size"]) * int(filters_pagination["page"])
        regx = re.compile(filters_pagination["search"], re.IGNORECASE)
        try:
            mongo.db["topics"].create_index([("title", pymongo.TEXT)])

            responses = mongo.db["topics"].aggregate(
                [
                    {
                        "$addFields": {
                            "is_match": {
                                "$regexMatch": {
                                    "input": "$title",
                                    "regex": regx,
                                },
                            }
                        }
                    },
                    {
                        "$match": {
                            "is_match": True
                        }
                    },
                    {
                        "$skip": skip
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
                                                    "$eq": ["$topic_id","$$id"]
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
                                                    "$eq": ["$is_memorized",True]
                                                },
                                                {
                                                    "$eq": ["$topic_id","$$id"]
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
                            "notes": {"$ifNull": ["$notes_counter.count",0]},
                            "notes_memorized": {"$ifNull": ["$notes_memorized_counter.count",0]}
                        }
                    }
                ])

            list_responses = list(responses)
            json_list_responses = list(map(lambda document: json.loads(json.dumps(document, default=lambda o: str(o))), list_responses))

            return json_list_responses
        except Exception as e:
            raise Exception("Error in find all: ", e)

    def find_topic_with_notes_info(self, topic_id):
        try:
            responses = mongo.db["topics"].aggregate([
                {
                    "$match": {
                        "_id": ObjectId(topic_id)
                    }
                },
                {
                    "$lookup": {
                        "from": "notes",
                        "let": {"id": "$_id"},
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$eq": ["$topic_id","$$id"]
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
                    }
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
                                            {"$eq": ["$topic_id", "$$id"]},
                                            {"$eq": ["$is_memorized", True]},
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
                    }
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
                        "notes": {"$ifNull": ["$notes_counter.count", 0]},
                        "notes_memorized": {"$ifNull": ["$notes_memorized_counter.count", 0]}
                    }
                }
            ])

            if responses is None:
                raise Exception("Error finding topic")

            list_responses = list(responses)
            if len(list_responses) == 0:
                return []

            json_list_responses = list(map(lambda document: json.loads(json.dumps(document, default=lambda o: str(o))), list_responses))

            return json_list_responses[0]
        except Exception as e:
            print(e)
            raise Exception("Error finding topic with notes info")


TopicServiceImpl = TopicService("topics")
