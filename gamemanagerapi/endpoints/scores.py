import cherrypy
from typing import List

from gamemanagerlib.business import matches, teams, scores
from gamemanagerapi.endpoints import scores_stroage, cy_tools


@cherrypy.expose
class Root(object):

    def format_scores(self, score: scores.Score) -> dict:

        if not scores:
            return []

        return {
            "id": score.id,
            "team_id": score.team_id,
            "game_id": score.match_id,
            "value": score.value
        }

    @cy_tools.uses_json
    def POST(self, team_id, game_id, value):

        scores_bll = scores.Business(scores_stroage)
        result = scores_bll.record_score(
            scores.Score(
                team_id,
                game_id,
                value=value
            )
        )

        return self.format_scores(score=result)

    @cy_tools.uses_json
    def GET(self, score_id, game_id=None, team_id=None, **kwargs):

        scores_bll = scores.Business(scores_stroage)
        result = scores_bll.get_store(
            id = score_id
        )

        return [self.format_scores(score) for score in result]