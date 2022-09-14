import json

from bson import json_util,ObjectId

from api.pojos.Filters import Filters
from api.services.crud import CrudService
from config.extensions import mongo


class NoteService(CrudService):
    def __init__(self, collection_name):
        super().__init__(collection_name)

    def find_all_by_topic_id(self, topic_id: str, filters: Filters):
        try:
            skip = filters["size"] * filters["page"]

            responses = mongo.db["notes"].aggregate(
                [
                    {
                        "$match": {
                            "topic_id": ObjectId(topic_id)
                        }
                    },
                    {
                        "$skip": skip
                    },
                    {
                        "$limit":  15
                    },
                    {
                        "$project": {
                            "_id":  1,
                            "title": 1,
                            "description": 1,
                            "is_liked": 1,
                            "is_memorized": 1,
                            "is_ignored": 1,
                            "topic_id": 1
                        }
                    }
                ]
            )

            list_responses = list(responses)
            json_list_responses = list(map(lambda document: json.loads(json.dumps(document, default=lambda o: str(o))), list_responses))

            return json_list_responses
        except Exception as e:
            print(e)
            raise Exception("Error in find all by topic id")


NoteServiceImpl = NoteService("notes")
