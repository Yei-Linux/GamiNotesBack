from api.services.crud import CrudService


class TopicService(CrudService):
    def __init__(self, collection_name):
        super().__init__(collection_name)


TopicServiceImpl = TopicService("topics")
