import cherrypy
import json
import functools


class Base(object):

    def OPTIONS(self):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = "*"
        cherrypy.response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE"
        cherrypy.response.headers["Access-Control-Allow-Headers"] = "Content-Type"


def uses_json(func):

    @functools.wraps(func)
    @cherrypy.tools.accept(media="application/json")
    def wrapper(*args, **kwargs):

        cherrypy.serving.response.headers['Content-Type'] = "application/json"

        kwargs = dict(kwargs)

        try:
            body = cherrypy.request.body.read()
            kwargs.update(json.loads(body))
        except (TypeError, AttributeError):
            pass

        return json.dumps(func(*args, **kwargs)).encode('utf8')

    return wrapper
