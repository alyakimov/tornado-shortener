from __future__ import absolute_import, division, print_function, with_statement

import tornado.web
from tornado.options import options
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class TemplateRendering:
    """
    A simple class to hold methods for rendering templates.
    """
    def render_template(self, template_name, **kwargs):
        template_dirs = []
        if self.settings.get('template_path', ''):
            template_dirs.append(
                self.settings["template_path"]
            )

        env = Environment(loader=FileSystemLoader(template_dirs))

        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(kwargs)
        return content


class BaseHandler(tornado.web.RequestHandler, TemplateRendering):

    def prepare(self):
        self.set_header("Content-Type", "text/html")

    def jinja_render(self, template_name, **kwargs):

        kwargs.update({
            'settings': self.settings,
            'options': options,
            'request': self.request,
            'xsrf_token': self.xsrf_token,
            'xsrf_form_html': self.xsrf_form_html,
            'static_url': self.static_url,
            'reverse_url': self.application.reverse_url
        })
        content = self.render_template(template_name, **kwargs)
        self.write(content)
