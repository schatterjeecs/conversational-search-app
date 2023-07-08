class DB:

    def __init__(self) -> None:
        self.db_data = ""

    def store_data(self, data):
        self.db_data = data

    def get_data(self):
        return self.db_data