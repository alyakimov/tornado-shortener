from __future__ import absolute_import, division, print_function, with_statement

import tornado.web
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from tornado.options import options
from shortener.handlers import base
from shortener.forms import forms
from shortener.backend import backend
from shortener.models import models


class MainHandler(base.BaseHandler):    
    @tornado.web.asynchronous
    def get(self):

        form = forms.ShotenerForm()

        params = {
            "form": form
        }

        self.jinja_render("index.html", **params)
        self.finish()

    @tornado.web.asynchronous
    def post(self):

        form = forms.ShotenerForm(self.request.arguments)

        if form.validate():
            db = backend.Backend.instance().get_session()

            try:
                short_uri = models.ShortURI()
                short_uri.full = form.uri.data
                short_uri.created = func.now()

                db.add(short_uri)
                db.commit()

                short_uri.generate_short_url()
                db.commit()

                params = {
                    "form": form,
                    "short_url": "{}/{}".format(options.domain_name, short_uri.short)
                }

                self.jinja_render('shorten.html', **params)
                self.finish()
                return

            finally:
                db.close()

        params = {
            "form": form
        }

        self.jinja_render("index.html", **params)
        self.finish()


class ApiHandler(base.BaseHandler):
    @tornado.web.asynchronous
    def post(self):

        form = forms.ShotenerForm(self.request.arguments)

        if form.validate():

            db = backend.Backend.instance().get_session()

            try:
                short_uri = models.ShortURI()
                short_uri.full = form.uri.data
                short_uri.created = func.now()

                db.add(short_uri)
                db.commit()

                short_uri.generate_short_url()
                db.commit()

                self.write("{}/{}".format(options.domain_name, short_uri.short))
                self.finish()
                return

            finally:
                db.close()

        else:
            self.send_error(400)


class InfoHandler(base.BaseHandler):
    @tornado.web.asynchronous
    def get(self, short):
        db = backend.Backend.instance().get_session()

        try:
            short_uri = db.query(models.ShortURI)\
                .filter(models.ShortURI.short == short)\
                .one()

            hits = db.query(func.strftime('%Y-%m-%d', models.Hit.created), func.count())\
                .filter(models.Hit.short_id == short_uri.id)\
                .group_by(func.strftime('%Y-%m-%d', models.Hit.created))\
                .all()

            params = {
                "short_uri": short_uri,
                "hits": hits
            }

            self.jinja_render("info.html", **params)
            self.finish()

        except NoResultFound:
            self.set_status(404)
            self.jinja_render("404.html")
            self.finish()
        finally:
            db.close()


class NotFoundHandler(base.BaseHandler):

    def get(self, *args, **kwargs):
        self.jinja_render("404.html")

    def post(self, *args, **kwargs):
        self.jinja_render("404.html")

    def put(self, *args, **kwargs):
        self.jinja_render("404.html")

    def delete(self, *args, **kwargs):
        self.jinja_render("404.html")

    def options(self, *args, **kwargs):
        self.jinja_render("404.html")