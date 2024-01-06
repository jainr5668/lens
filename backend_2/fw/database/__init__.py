import os
import copy
import sqlite3
from pymongo import MongoClient

from .models.sqlite import Sqlite3_Client
from .models.mongoDb import MongoDB_CLient
from .authentication import Authentication


class Database:
    __DATABASETYPE = "sqlite3"
    __authentication = None
    __DATABASENAME = "sqlite.db"
    __CONNECTION_STRING = (
        "mongodb+srv://lens_rw:hCFgvYUeY62LHeJ3@lens-mdb.ljxkjx4.mongodb.net/"
    )
    DATA_PATH = os.path.realpath(
        os.path.dirname(os.path.realpath(__file__)) + "/../data/database"
    )

    def __init__(self, common_instance):
        self.__common_instance = common_instance
        if self.__DATABASETYPE == "sqlite3":
            self.__con = sqlite3.connect(self.__DATABASENAME, check_same_thread=False)
            self.__create_tables()
            self.__con = Sqlite3_Client(self.__con)
        elif self.__DATABASETYPE == "mongodb":
            self.__con = MongoDB_CLient(self.__CONNECTION_STRING)

    def __create_tables(self):
        queries = self.__common_instance.utility.load_file(
            self.DATA_PATH, "query.json"
        )["creating_tables"]
        for query in queries.items():
            self.__con.execute(query[1])

    @property
    def authentication(self):
        if self.__authentication is None:
            self.__authentication = Authentication(self.__con)
        return self.__authentication

