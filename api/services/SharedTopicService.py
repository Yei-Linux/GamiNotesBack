from datetime import datetime
from config.extensions import mongo


class SharedTopicService:
    def create_temporal_shared_topic(self, topic, notes, user):
        expiration_date = datetime(2022,9,26,23,59,59)

        mongo.db["shared_topics"].insert_one({
            "username": user.username,
            "topic_title": topic.title,
            "user_limit": 0,
            "create_at": "",
            "notes": notes
        })

        mongo.db["shared_topics"].createIndex({"create_at": 1}, {
            expiration_date: 86400
        })