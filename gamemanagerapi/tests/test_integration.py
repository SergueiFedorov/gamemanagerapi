import unittest
import cherrypy
import json

from gamemanagerapi.endpoints import games, player, teams, scores


class Tests(unittest.TestCase):

    def _create_game(self):

        controller = games.Root()
        result = json.loads(controller.POST(name="test_game"))

        return result

    def _create_single_player_game(self):

        game = self._create_game()

        player_controller = player.Root()
        teams_controller = teams.Root()
        games_controller = games.Root()

        new_player = json.loads(player_controller.POST(name="player"))
        new_team = json.loads(teams_controller.POST(name="team"))

        result = json.loads(teams_controller.players.POST(team_id=new_team["id"], player_id=new_player["id"]))

        self.assertTrue(result)

        result = games_controller.teams.POST(game["id"], new_team["id"])

        self.assertTrue(result)

        return game, new_team, new_player

    def test_create_game(self):

        result = self._create_game()
        self.assertIsNotNone(result["id"])

    def test_create_single_player_game(self):

        (game, new_team, new_player) = self._create_single_player_game()

        games_controller = games.Root()
        team_controller = teams.Root()
        player_controller = player.Root()

        saved_game = json.loads(games_controller.GET(id=game["id"]))

        # Make sure game ids match
        self.assertEqual(saved_game["id"], game["id"])
        self.assertTrue(new_team["id"] in saved_game["team_ids"])

        saved_player = json.loads(player_controller.GET(new_player["id"]))

        self.assertEqual(saved_player["id"], new_player["id"])

        saved_team = json.loads(team_controller.GET(new_team["id"]))

        self.assertEqual(saved_team["id"], new_team["id"])
        self.assertTrue(saved_player["id"] in saved_team["player_ids"])

    def test_game_not_found(self):

        games_controller = games.Root()
        result = games_controller.GET(id=1)

        self.assertTrue(not json.loads(result))

    def test_team_not_found(self):

        team_controller = teams.Root()
        result = team_controller.GET(id=1)

        self.assertTrue(not json.loads(result))

    def test_player_not_found(self):

        player_contoller = player.Root()
        result = player_contoller.GET(id=1)

        self.assertTrue(not json.loads(result))

    def test_assign_score(self):

        games_controller = games.Root()
        teams_controller = teams.Root()
        scores_controller = scores.Root()

        game = json.loads(games_controller.POST("test"))
        team = json.loads(teams_controller.POST("test"))

        score = json.loads(scores_controller.POST(game_id=game["id"], team_id=team["id"], value="1"))

        self.assertIsNotNone(score["id"])

        obtained_score = json.loads(scores_controller.GET(score["id"]))

        self.assertEqual(obtained_score[0]["id"], score["id"])