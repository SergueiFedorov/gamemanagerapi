import cherrypy

import gamemanagerapi.endpoints.player
import gamemanagerapi.endpoints.teams
import gamemanagerapi.endpoints.games
import gamemanagerapi.endpoints.scores


if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }

    player = cherrypy.tree.mount(gamemanagerapi.endpoints.player.Root(), "/player", conf)
    teams = cherrypy.tree.mount(gamemanagerapi.endpoints.teams.Root(), "/team", conf)
    games = cherrypy.tree.mount(gamemanagerapi.endpoints.games.Root(), "/game", conf)
    scores = cherrypy.tree.mount(gamemanagerapi.endpoints.scores.Root(), "/score", conf)

    cherrypy.engine.start()
    cherrypy.engine.block()
