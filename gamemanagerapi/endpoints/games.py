import cherrypy

from gamemanagerlib.business import matches, teams
from gamemanagerapi.endpoints import games_storage, teams_storage, cy_tools
from gamemanagerapi.endpoints.cy_tools import Base


@cherrypy.expose
class Teams(Base):

    @cy_tools.uses_json
    def POST(self, id, team_id, *args, **kwargs):
        matches_bll = matches.Business(games_storage)
        teams_bll = teams.Business(teams_storage)

        errors = []
        if not matches_bll.find_match(id):
            errors.append("Cannot find game %s" % (id,))
        if not teams_bll.get_team(team_id):
            errors.append("Cannot find team %s" % (id,))

        if not errors:
            matches_bll.assign_team(id, team_id)

        return {"errors": errors}


@cherrypy.expose
@cherrypy.popargs('id')
class Root(Base):

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
    def POST(self, name, *args, **kwargs) -> dict:

        bll = matches.Business(games_storage)
        result = bll.create_match(matches.Match(name=name))
        return self.format_game(result)

    @cy_tools.uses_json
    def GET(self, id):

        bll = matches.Business(games_storage)
        result = bll.find_match(id=id)
        return self.format_game(result)