from http import HTTPStatus

from flasgger import swag_from
from flask import Blueprint,request

from api.pojos.responses.Response import Response
from api.schemas.ResponseSchema import ResponseSchema
from api.schemas.TopicSchema import TopicSchema
from api.services.topics import TopicServiceImpl

topics_api = Blueprint("api",__name__)


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
    try:
        topics = TopicServiceImpl.find_all()

        response = Response(data=topics,message="Topics got successfully!")
        return ResponseSchema().dump(response),200
    except Exception as e:
        print(e)
        response = Response(data=None,message="There was an error")
        return ResponseSchema().dump(response),500


@topics_api.route("/<id>", methods=["GET"])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Find topic by id',
            'schema': TopicSchema
        }
    }
})
def find_by_id(id: str):
    try:
        topic = TopicServiceImpl.find_by_id(id)
        message = "Topic got successfully!" if topic is not None else "There is not topic with this id"

        response = Response(data=topic, message=message)
        return ResponseSchema().dump(response), 200
    except Exception as e:
        print(e)
        response = Response(data=None, message="There was an error")
        return ResponseSchema().dump(response), 500


@topics_api.route("/", methods=["POST"])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Create topic',
            'schema': TopicSchema
        }
    }
})
def create():
    try:
        data = request.get_json()
        topic = TopicServiceImpl.create(data)

        response = Response(data=topic,message="Topic was created successfully!")
        return ResponseSchema().dump(response),200
    except Exception as e:
        print(e)
        response = Response(data=None,message="There was an error")
        return ResponseSchema().dump(response),500


@topics_api.route("/<id>" ,methods=["PUT"])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Update topic',
            'schema': TopicSchema
        }
    }
})
def update(id):
    try:
        data = request.get_json()
        topic = TopicServiceImpl.update_by_id(id, data)

        response = Response(data=topic, message="Topic was updated successfully!")
        return ResponseSchema().dump(response), 200
    except Exception as e:
        print(e)
        response = Response(data=None,message="There was an error")
        return ResponseSchema().dump(response),500


@topics_api.route("/<id>" ,methods=["DELETE"])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Delete topic',
            'schema': TopicSchema
        }
    }
})
def delete(id: str):
    try:
        TopicServiceImpl.delete_by_id(id)

        response = Response(data=None,message="Topic was deleted successfully!")
        return ResponseSchema().dump(response), 200
    except Exception as e:
        print(e)
        response = Response(data=None,message="There was an error")
        return ResponseSchema().dump(response), 500