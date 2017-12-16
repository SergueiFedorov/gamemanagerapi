import cherrypy

from gamemanagerlib.business import players
from gamemanagerlib.business import teams

from gamemanagerapi.endpoints import teams_storage, player_storage, cy_tools


@cherrypy.expose
class Players(object):

    @cy_tools.uses_json
    def POST(self, team_id, player_id, *args, **kwargs):

        teams_bll = teams.Business(storage=teams_storage)
        player_bll = players.Business(storage=player_storage)

        errors = []
        if not teams_bll.get_team(team_id):
            errors.append("Cannot find team %s" % (team_id,))
        if not player_bll.get_player(player_id):
            errors.append("Cannot find player %s" % (player_id,))

        result = teams_bll.assign_player(int(team_id), int(player_id))

        return {
            "errors": errors
        }


@cherrypy.expose
@cherrypy.popargs('id')
class Root(object):

    def __init__(self):

        self.players = Players()

    @staticmethod
    def format_team(team: teams.Team) -> dict:
        if not team:
            return {}

        return {
            "id": team.id,
            "name": team.name,
            "player_ids": team.player_ids
        }

    @cy_tools.uses_json
    def POST(self, name, **kwargs):

        team_bll = teams.Business(storage=teams_storage)
        result = team_bll.create_team(teams.Team(name=name))

        return self.format_team(result)

    @cy_tools.uses_json
    def GET(self, id):

        team_bll = teams.Business(storage=teams_storage)
        result = team_bll.get_team(id=int(id))

        return self.format_team(result)