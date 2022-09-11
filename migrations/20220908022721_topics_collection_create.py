from bson import ObjectId
from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):
    def upgrade(self):
        validator = {"$jsonSchema": {
            "description": "Topic Collection for topics parent",
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "created_at": {"type": "string"},
                "updated_at": {"type": "string"},
                "delete_at": {"type": "string"},

                "user_id": {"bsonType": "objectId"}
            },
            "required": ["title", "user_id"],
            "dependencies": {}}}

        self.db.create_collection("topics", validator=validator)

    def downgrade(self):
        pass
