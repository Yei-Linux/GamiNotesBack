import json
from datetime import datetime

from api.services.crud import CrudService
from config.extensions import mongo
from config.server_config import server_config


class SharedTopicService(CrudService):
    def __init__(self,collection_name):
        super().__init__(collection_name)

    def create_temporal_shared_topic(self,topic,notes,user):
        created_at = datetime.utcnow()
        try:
            with mongo.db.client.start_session() as session:
                mongo.db["shared_topics"].create_index(keys="create_at",
                                                       expireAfterSeconds=server_config["expiration_time_ttl"],
                                                       session=session)
                document = {
                    "username": user["username"],
                    "topic_title": topic["title"],
                    "user_limit": 0,
                    "create_at": created_at,
                    "notes": notes
                }
                mongo.db["shared_topics"].insert_one(document)

                document_response = {
                    "_id": document["_id"],
                    "username": document["username"],
                    "topic_title": document["topic_title"],
                    "user_limit": document["user_limit"],
                    "create_at": created_at,
                }

                shared_topic_created_serialized = json.loads(json.dumps(document_response, default=lambda o: str(o)))
                return shared_topic_created_serialized
        except Exception as error:
            print(error)
            raise Exception("Failed on create shared topic with index")


SharedTopicServiceImpl = SharedTopicService("shared_topics")
