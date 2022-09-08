from flask_marshmallow import Schema
from marshmallow.fields import Str


class TopicSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["title", "description"]

    title = Str()
    description = Str()
