from api.services.crud import CrudService


class NoteService(CrudService):
    def __init__(self, collection_name):
        super().__init__(collection_name)


NoteServiceImpl = NoteService("notes")
