import cherrypy

import gamemanagerapi.endpoints.player
import gamemanagerapi.endpoints.teams
import gamemanagerapi.endpoints.games

if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }

    cherrypy.tree.mount(gamemanagerapi.endpoints.player.Root(), "/players", conf)
    cherrypy.tree.mount(gamemanagerapi.endpoints.teams.Root(), "/teams", conf)
    cherrypy.tree.mount(gamemanagerapi.endpoints.games.Root(), "/games", conf)

    cherrypy.engine.start()
    cherrypy.engine.block()
