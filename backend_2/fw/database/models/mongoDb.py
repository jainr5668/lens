

from pymongo import MongoClient


class MongoDB_CLient:
    def __init__(self, connection_string):
        self.__client = MongoClient(connection_string)
        self.__client = self.__client["lens_db"]

    def table_columns(self, table_name):
        pass

    def insert(self, table_name, data, conditions=None):
        try:
            self.__client[table_name].insert_one(copy.deepcopy(data))
        except Exception as e:
            return {"error": e}

    def fetch_all(self, table_name, conditions):
        return [data for data in self.__client[table_name].find(conditions)]

    def fetch_one(self, table_name, **conditions):
        print(conditions)
        return self.__client[table_name].find_one(conditions)

    def delete(self, table_name, **conditions):
        pass
