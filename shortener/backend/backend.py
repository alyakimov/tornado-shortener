from __future__ import absolute_import, division, print_function, with_statement

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from tornado.options import options


class Backend(object):
    def __init__(self):
        settings = {
            "drivername": options.db_drivername,
            "username": options.db_username,
            "password": options.db_password,
            "host": options.db_host,
            "port": options.db_port,
            "database": options.db_database
        }

        engine = create_engine(
            URL(**settings),
            pool_size=options.db_pool_size,
            pool_recycle=3600,
            echo=options.tornado_debug,
            echo_pool=options.tornado_debug)

        self._session = sessionmaker(bind=engine, expire_on_commit=False)

    @classmethod
    def instance(cls):
        """Singleton like accessor to instantiate backend object"""
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def get_session(self):
        return self._session()
