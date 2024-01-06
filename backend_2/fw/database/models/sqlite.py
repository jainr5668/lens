class Sqlite3_Client:
    def __init__(self, db):
        self.__db = db

    def table_columns(self, table_name):
        columns = []
        for column in self.__db.execute(f"PRAGMA table_info({table_name});"):
            columns.append(column[1])
        return columns

    def insert(self, table_name, data):
        query = "INSERT INTO {} ({}) VALUES {};"
        values = tuple([f"{value}" for value in data.values()])
        query = query.format(table_name, ", ".join(data.keys()), values)
        try:
            self.__db.execute(query)
            self.__db.commit()
        except Exception as e:
            return ("Error while inserting into {}:".format(table_name), e)

    def __generate_condition(self, conditions):
        condition_list = []
        condition_str = ""
        for condition in conditions:
            condition_instance_str = condition["key"] + " = "
            if condition["type"] == "string":
                condition["value"] = '"' + str(condition["value"]) + '"'
            condition_instance_str += condition["value"]
            condition_list.append(condition_instance_str)
        if len(condition_list) > 0:
            condition_str = "WHERE " + " AND ".join(condition_list)
        return condition_str

    def fetch_one(self, table_name, conditions=[]):
        try:
            condition = self.__generate_condition(conditions)
            query = f"select * from {table_name} {condition};"
            values = list(self.__db.execute(query).fetchone())
            data = {}
            for key, value in zip(self.table_columns(table_name), values):
                data[key] = value
            return data
        except:
            return None

    def delete(self, table_name, conditions=[]):
        try:
            condition = self.__generate_condition(conditions)
            query = f"DELETE from {table_name} {condition};"
            values = list(self.__db.execute(query))
            self.__db.commit()
            data = {}
            for key, value in zip(self.table_columns(table_name), values):
                data[key] = value
            return data
        except Exception as e:
            return None
