from http import HTTPStatus

from flasgger import swag_from
from flask import request
from flask_restful import Resource

from api.pojos.requests.SharedTopicCreate import SharedTopicCreate
from api.schemas.ResponseSchema import ResponseSchema
from api.services.NoteService import NoteService
from api.services.SharedTopicService import SharedTopicService
from api.services.TopicService import TopicService
from api.services.UserService import UserService


class SharedTopicListResource(Resource):
    topic_service = TopicService(collection_name="topic")
    note_service = NoteService(collection_name="note")
    user_service = UserService(collection_name="user")
    shared_topic_service = SharedTopicService()

    @swag_from({
        'responses': {
            HTTPStatus.OK.value: {
                'description': 'Find note by id',
                'schema': ResponseSchema
            }
        }
    })
    def post(self):
        body = request.get_json(force=True)
        body_parse = SharedTopicCreate(topic_id=body["topic_id"])


        try:
            topic = self.topic_service.find_by_id(body_parse.topic_id)
            user = self.user_service.find_by_id(topic["user_id"])
            notes = self.note_service.find_all_by_topic_id(body_parse.topic_id,user)
            self.shared_topic_service.create_temporal_shared_topic(topic,notes,user)
        except Exception as error:
            print(error)
            return
