import cherrypy
import json
import functools


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
