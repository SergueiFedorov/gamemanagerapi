import cherrypy

from gamemanagerlib.business import players
from gamemanagerlib.business import teams

from gamemanagerapi.endpoints import player_storage, games_storage, teams_storage, cy_tools


@cherrypy.expose
class Teams(object):

    @staticmethod
    def format_team(team : teams.Team) -> dict:
        return {
            "id": team.id,
            "name": team.name
        }

    @cy_tools.uses_json
    def GET(self, player_id):

        team_business = teams.Business(storage=teams_storage)
        result = team_business.get_player_teams(player_id)

        return [self.format_team(team) for team in result]


@cherrypy.expose
@cherrypy.popargs('player_id')
class Root(object):

    def __init__(self):
        self.teams = Teams()

    @staticmethod
    def format_player(player: players.Player) -> dict:

        if not player:
            return {}

        return {
            "id": player.id,
            "name": player.name
        }

    @cy_tools.uses_json
    def GET(self, player_id):

        bll = players.Business(player_storage)
        player = bll.get_player(int(player_id))

        return self.format_player(player[0] if player else None)

    @cy_tools.uses_json
    def POST(self, name):
        bll = players.Business(player_storage)
        player = bll.create_player(players.Player(name=name))

        return self.format_player(player)