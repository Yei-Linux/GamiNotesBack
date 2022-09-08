from flasgger import Swagger
from flask import Flask

from api.controllers.topics import topics_api
from config.extensions import mongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://jesus:123@127.0.0.1:27017/gami_notes?authSource=admin"
app.config["SWAGGER"] = {
    'title':  'Flask API Starter Kit'
}

swagger = Swagger(app)
mongo.init_app(app)

app.register_blueprint(topics_api, url_prefix="/gami-notes/topics")


if __name__ == '__main__':
    app.run()
