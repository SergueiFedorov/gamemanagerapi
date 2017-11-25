import cherrypy

from gamemanagerlib.business import matches, teams
from gamemanagerapi.endpoints import games_storage, teams_storage, cy_tools


class Teams(object):

    @cy_tools.uses_json
    def POST(self, game_id, team_id):
        matches_bll = matches.Business(games_storage)
        teams_bll = teams.Business(teams_storage)

        errors = []
        if not matches_bll.find_match(game_id):
            errors.append("Cannot find game %s" % (game_id,))
        if not teams_bll.get_team(team_id):
            errors.append("Cannot find team %s" % (team_id,))

        result = matches_bll.assign_team(game_id, team_id)

        return {"success": result}


@cherrypy.expose
@cherrypy.popargs('game_id')
class Root(object):

    def __init__(self):
        self.teams = Teams()

    @staticmethod
    def format_game(game: matches.Match) -> dict:

        if not game:
            return {}

        return {
            "id": game.id,
            "name": game.name,
            "team_ids": game.team_ids
        }

    @cy_tools.uses_json
    def POST(self, name):

        bll = matches.Business(games_storage)
        result = bll.create_match(matches.Match(name=name))
        return self.format_game(result)

    @cy_tools.uses_json
    def GET(self, game_id):

        bll = matches.Business(games_storage)
        result = bll.find_match(id=game_id)
        return self.format_game(result)