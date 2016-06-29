from __future__ import absolute_import, division, print_function, with_statement

import os.path
from tornado.options import define

# domain
define("domain_name", default="http://exmpl.org", help="domain name")

# tornado
define("tornado_port", default="8080", help="tornado port")
define("tornado_debug", default=True, help="debug mode")
define("template_path", default=os.path.join(os.path.dirname(__file__), 'templates'), help="Template path")
define("cookie_secret", default="61oETzL3QAGaYdkDLr4ELweJJFuYh7EQnp2XdTP1o/Vo=", help="cookie secret")

# database
define("db_drivername", default="postgresql", help="connection drivername")
define("db_host", default="localhost", help="connection host")
define("db_port", default="5432", help="connection port")
define("db_username", default="shortener_user", help="connection username")
define("db_password", default="shortener_pass", help="connection password")
define("db_database", default="shortener", help="connection database")
define("db_pool_size", default=8, help="connection pool size")