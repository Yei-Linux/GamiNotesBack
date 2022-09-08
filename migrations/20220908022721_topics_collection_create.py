from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):
    def upgrade(self):
        validator = {"$jsonSchema": {
            "description": "Topic Collection for topics parent",
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
            },
            "required": ["title"],
            "dependencies": {}}}

        self.db.create_collection("topics", validator=validator)

    def downgrade(self):
        pass
