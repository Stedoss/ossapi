from unittest import TestCase

from tests import api_v1

class TestGetUser(TestCase):
    def test_deserialize(self):
        r = api_v1.get_user("tybug2")

        self.assertEqual(r.username, "tybug2")
        self.assertEqual(api_v1.get_user(12092800).username, "tybug2")

class TestGetBeatmaps(TestCase):
    def test_deserialize(self):
        api_v1.get_beatmaps(beatmapset_id=1051305)
        api_v1.get_beatmaps(beatmap_id=221777)

class TestGetUserBest(TestCase):
    def test_deserialize(self):
        api_v1.get_user_best(12092800)

class TestGetReplay(TestCase):
    def test_deserialize(self):
        r1 = api_v1.get_replay(beatmap_id=221777, user=2757689)
        r2 = api_v1.get_replay(score_id=2828620518)

        self.assertEqual(len(r1), 155328)
        self.assertEqual(len(r2), 141068)

class TestGetScores(TestCase):
    def test_deserialize(self):
        api_v1.get_scores(221777)
        api_v1.get_scores(221777, user="tybug2")

class TestGetUserRecent(TestCase):
    def test_deserialize(self):
        api_v1.get_user_recent(12092800)

class TestGetMatch(TestCase):
    def test_deserialize(self):
        api_v1.get_match(69063884)
