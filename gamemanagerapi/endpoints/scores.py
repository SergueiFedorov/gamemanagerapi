import cherrypy

from gamemanagerlib.business import matches, teams, scores
from gamemanagerapi.endpoints import scores_stroage, cy_tools


@cherrypy.expose
class Root(object):

    @staticmethod
    def format_score(score: scores.Score) -> dict:

        if not scores:
            return {}

        return {
            "id": score.id,
            "team_id": score.team_id,
            "game_id": score.match_id,
            "value": score.value
        }

    @cy_tools.uses_json
    def POST(self, team_id, game_id, value, **kwargs):

        scores_bll = scores.Business(scores_stroage)
        result = scores_bll.record_score(
            scores.Score(
                team_id,
                game_id,
                value=value
            )
        )

        return [self.format_score(score=result)]

    @cy_tools.uses_json
    def GET(self, score_id=None, game_id=None, team_id=None, **kwargs):

        scores_bll = scores.Business(scores_stroage)

        result = None
        if score_id:
            result = scores_bll.get_store(
                id = score_id
            )
        elif game_id and team_id:
            result = scores_bll.get_scores_for_match(
                game_id,
                team_id
            )

        return [self.format_score(score) for score in result]
