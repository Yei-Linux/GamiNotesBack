from http import HTTPStatus

from flasgger import swag_from
from flask import request
from flask_restful import Resource

from api.pojos.requests.NoteUpdate import NoteUpdate
from api.resources.base.BaseSingleResource import BaseSingleResource
from api.schemas.ResponseSchema import ResponseSchema
from api.services.NoteService import NoteServiceImpl


class NoteResource(Resource):
    base_single_resource = BaseSingleResource("note", NoteServiceImpl)

    @swag_from({
        'responses': {
            HTTPStatus.OK.value: {
                'description': 'Find note by id',
                'schema': ResponseSchema
            }
        }
    })
    def get(self, note_id):
        return self.base_single_resource.get(note_id)

    @swag_from({
        'responses': {
            HTTPStatus.OK.value: {
                'description': 'Update note by id',
                'schema': ResponseSchema
            }
        }
    })
    def put(self, note_id):
        title, description, is_liked, is_memorized, is_ignored = request.get_json(force=True).values()
        body_parse = NoteUpdate(title, description, is_liked, is_memorized, is_ignored)

        return self.base_single_resource.put(note_id, vars(body_parse))

    @swag_from({
        'responses': {
            HTTPStatus.OK.value: {
                'description': 'Delete note by id',
                'schema': ResponseSchema
            }
        }
    })
    def delete(self, note_id):
        return self.base_single_resource.delete(note_id)