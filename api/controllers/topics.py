from http import HTTPStatus

from flasgger import swag_from
from flask import Blueprint

from api.pojos.responses.Response import Response
from api.schemas.ResponseSchema import ResponseSchema
from api.schemas.TopicSchema import TopicSchema
from config.extensions import mongo

topics_api = Blueprint("api", __name__)


@topics_api.route("/", methods=["GET"])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Find all topics',
            'schema': TopicSchema
        }
    }
})
def find_all():
    topics = mongo.db.topics.find({})
    response = Response(data=topics, message="Topics got successfully!")
    return ResponseSchema().dump(response), 200
