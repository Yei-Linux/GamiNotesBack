from typing import Any

from flask_marshmallow import Schema
from marshmallow.fields import Str, Dict


class ResponseSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["data", "message"]

    data = Dict()
    message = Str()
