from gamemanagerlib.storage.interface import Record


class User(Record):

    def __init__(self):
        super(User, self).__init__()
        pass


class Business(object):

    def __init__(self, storage):
        self.storage = storage

    def create_user(self, user: User) -> User:
        return self.storage.read(id=user.id)
