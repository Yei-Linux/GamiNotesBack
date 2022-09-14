from flasgger import Swagger
from flask import Flask
from flask_restful import Api

from api.resources.note.NoteListResource import NoteListResource
from api.resources.note.NoteResource import NoteResource
from api.resources.topic.TopicResource import TopicResource
from api.resources.topic.TopicListResource import TopicListResource
from api.resources.topic.TopicWithNotesResource import TopicWithNotesResource
from api.resources.user.UserListResource import UserListResource
from api.resources.user.UserResource import UserResource
from config.extensions import mongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

api = Api(app, prefix="/gami-notes/api/v1")


app.config["MONGO_URI"] = "mongodb://jesus:123@127.0.0.1:27017/gami_notes?authSource=admin"
app.config["SWAGGER"] = {
    'title': 'Flask API Starter Kit'
}

swagger = Swagger(app)
mongo.init_app(app)

api.add_resource(TopicWithNotesResource, "/topics/<topic_id>/notes")
api.add_resource(TopicResource, "/topics/<topic_id>")
api.add_resource(TopicListResource, "/topics")

api.add_resource(UserResource, "/users/<user_id>")
api.add_resource(UserListResource, "/users")

api.add_resource(NoteResource, "/notes/<note_id>")
api.add_resource(NoteListResource, "/notes")

if __name__ == '__main__':
    app.run()
