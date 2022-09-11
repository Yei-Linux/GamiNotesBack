from bson import ObjectId
from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):
    def upgrade(self):
        self.db.get_collection("topics").insert_many([
            {
                "_id": ObjectId("631cdb1b250a87dd50fb5080"),
                "title": "Roman History",
                "description": "Related to all events occurred in monarchy period since Octavio government",
                "user_id": ObjectId("631cda65e254720368a68d40")
            },
            {
                "_id": ObjectId("631cdb1b250a87dd50fb5081"),
                "title": "Biology",
                "description": "Related to scientific information",
                "user_id": ObjectId("631cda65e254720368a68d40")
            },
            {
                "_id": ObjectId("631cdb1b250a87dd50fb5082"),
                "title": "Programming",
                "description": "Related to basic programming concepts",
                "user_id": ObjectId("631cda65e254720368a68d41")
            },
        ])

    def downgrade(self):
        pass
