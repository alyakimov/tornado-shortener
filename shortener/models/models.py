from __future__ import absolute_import, division, print_function, with_statement

import math
import string
from sqlalchemy import Column, String, DateTime, BigInteger
from sqlalchemy import UniqueConstraint, ForeignKey, Sequence, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ShortURI(Base):
    __tablename__ = "short_uri"

    id = Column(BigInteger, Sequence('short_uri_seq'), primary_key=True, nullable=False)
    short = Column(String(200), nullable=True, index=True)
    full = Column(String(4000), nullable=False)
    created = Column(DateTime(timezone=True), nullable=False)

    hits = relationship("Hit", backref="short_uri")

    __table_args__ = (
        UniqueConstraint('short', name='_short_uri_uc'),
    )

    def generate_short_url(self):
        out = ""
        number = self.id
        s = string.ascii_lowercase + string.ascii_uppercase + string.digits

        while number > 30:
            key = int(number) % 31
            number = math.floor(int(number) / 31) - 1
            out = s[key] + out

        self.short = s[int(number)] + out


class Hit(Base):
    __tablename__ = "hits"

    id = Column(BigInteger, Sequence('hits_seq'), primary_key=True, nullable=False)
    short_id = Column(BigInteger, ForeignKey(ShortURI.id), nullable=False)
    ip = Column(String(15), nullable=True)
    referrer = Column(String(4000), nullable=True)
    created = Column(DateTime(timezone=True), nullable=False)

    def __init__(self, ip, referrer):
        self.ip = ip
        self.referrer = referrer
        self.created = func.now()


if __name__ == '__main__':
    import os
    import sys

    sys.path.append(os.getcwd())

    from tornado.options import options
    from sqlalchemy import create_engine
    from sqlalchemy.engine.url import URL
    import shortener.settings

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
        echo=options.tornado_debug,
        echo_pool=options.tornado_debug
    )

    Base.metadata.create_all(engine)
