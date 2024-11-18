import logging
import os
import threading
from redash.query_runner import (
    BaseSQLQueryRunner,
    InterruptException,
    TYPE_DATE,
    TYPE_DATETIME,
    TYPE_FLOAT,
    TYPE_INTEGER,
    TYPE_STRING,
    register,
)

import MySQLdb



types_map = {
    0: TYPE_FLOAT,
    1: TYPE_INTEGER,
    2: TYPE_INTEGER,
    3: TYPE_INTEGER,
    4: TYPE_FLOAT,
    5: TYPE_FLOAT,
    7: TYPE_DATETIME,
    8: TYPE_INTEGER,
    9: TYPE_INTEGER,
    10: TYPE_DATE,
    12: TYPE_DATETIME,
    15: TYPE_STRING,
    16: TYPE_INTEGER,
    246: TYPE_FLOAT,
    253: TYPE_STRING,
    254: TYPE_STRING,
}


class Result:
    def __init__(self):
        pass

class Starrocks(BaseSQLQueryRunner):
    noop_query = "SELECT 1"


    @classmethod
    def configuration_schema(cls):
        schema = {
            "type": "object",
            "properties": {
                "host": {"type": "string", "default": "127.0.0.1"},
                "user": {"type": "string"},
                "password": {"type": "string"},
                "database": {"type": "string"},
                "port": {"type": "number", "default": 3306},
                "connection_timeout": {"type": "number", "default": 60},
                "charset": {"type": "string", "default": "utf8"},
                "use_unicode": {"type": "boolean", "default": True},
                "autocommit": {"type": "boolean", "default": False},
            },
            "order": [
                "host",
                "port",
                "user",
                "password",
                "database",
                "connection_timeout",
                "charset",
                "use_unicode",
                "autocommit",
            ],
            "required": ["database"],
            "secret": ["password"]
        }

        return schema
    
    def _connection(self):
        params = dict(
            host=self.configuration.get("host", ""),
            user=self.configuration.get("user", ""),
            password=self.configuration.get("password", ""),
            database=self.configuration.get("database", ""),
            port=self.configuration.get("port", 3306),
            charset=self.configuration.get("charset", "utf8"),
            use_unicode=self.configuration.get("use_unicode", True),
            connect_timeout=self.configuration.get("connect_timeout", 60),
            autocommit=self.configuration.get("autocommit", True),
        )

        connection = MySQLdb.connect(**params)

        return connection

        
    def run_query(self, query, user):
        ev = threading.Event()
        thread_id = ""
        r = Result()
        t = None

        try:
            connection = self._connection()
            thread_id = connection.thread_id()
            t = threading.Thread(target=self._run_query, args=(query, user, connection, r, ev))
            t.start()
            while not ev.wait(1):
                pass
        except (KeyboardInterrupt, InterruptException, JobTimeoutException):
            self._cancel(thread_id)
            t.join()
            raise


        return r.data, r.error
    
    def _run_query(self, query, user, connection, r, ev):
        try:
            cursor = connection.cursor()
            cursor.execute(query)

            data = cursor.fetchall()
            desc = cursor.description

            while cursor.nextset():
                if cursor.description is not None:
                    data = cursor.fetchall()
                    desc = cursor.description


            if desc is not None:
                columns = self.fetch_columns([(i[0], types_map.get(i[1], None)) for i in desc])
                rows = [dict(zip((column["name"] for column in columns), row)) for row in data]

                data = {"columns": columns, "rows": rows}
                r.data = data
                r.error = None

            else:
                r.data = None
                r.error = "No data was returned."

            cursor.close()
        except MySQLdb.Error as e:
            if cursor:
                cursor.close()
            r.data = None
            r.error = e.args[1]
        finally:
            ev.set()
            if connection:
                connection.close()


    def _cancel(self, thread_id):
        connection = None
        cursor = None
        error = None

        try:
            connection = self._connection()
            cursor = connection.cursor()
            query = "KILL %d" % (thread_id)
            cursor.execute(query)
        except MySQLdb.Error as e:
            if cursor:
                cursor.close()
            error = e.args[1]
        finally:
            if connection:
                connection.close()

        return error
    

register(Starrocks)