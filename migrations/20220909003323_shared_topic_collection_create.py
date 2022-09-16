from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):
    def upgrade(self):
        validator = {"$jsonSchema": {
            "description": "Shared Topic Collection",
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "topic_title": {"type": "string"},
                "notes": {
                    "type": "array",
                    "items": {
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"}
                        }
                    }
                },

                "user_limit": {"type": "number"},
                "create_at": {"bsonType": "date"},
            },
            "required": ["topic_title","username","notes","expiration_date"],
            "dependencies": {}}}

        self.db.create_collection("shared_topics",validator=validator)

    def downgrade(self):
        pass
