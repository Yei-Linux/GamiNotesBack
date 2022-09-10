from http import HTTPStatus

from flasgger import swag_from
from flask import request
from flask_restful import Resource

from api.resources.base.BaseAllResource import BaseAllResource
from api.schemas.ResponseSchema import ResponseSchema
from api.services.TopicService import TopicServiceImpl


class TopicListResource(Resource):
    base_single_resource = BaseAllResource("topics", TopicServiceImpl)

    @swag_from({
        'responses': {
            HTTPStatus.OK.value: {
                'description': 'Get topics',
                'schema': ResponseSchema
            }
        }
    })
    def get(self):
        return self.base_single_resource.get()

    @swag_from({
        'responses': {
            HTTPStatus.OK.value: {
                'description': 'Create a new one topic',
                'schema': ResponseSchema
            }
        }
    })
    def post(self):
        return self.base_single_resource.post(request.get_json())
