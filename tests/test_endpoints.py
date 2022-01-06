import unittest
from datetime import datetime
from pathlib import Path
from unittest import TestCase

from ossapi import (RankingType, BeatmapsetEventType, AccessDeniedError,
    InsufficientScopeError)

from tests import (api, client_id, client_secret, DEV_HOST, dev_client_secret,
    dev_client_id)

class TestBeatmapsetDiscussionPosts(TestCase):
    def test_deserialize(self):
        api.beatmapset_discussion_posts()

class TestUserRecentActivity(TestCase):
    def test_deserialize(self):
        api.user_recent_activity(12092800)

class TestSpotlights(TestCase):
    def test_deserialize(self):
        api.spotlights()

class TestUserBeatmaps(TestCase):
    def test_deserialize(self):
        api.user_beatmaps(user_id=12092800, type_="most_played")

class TestUserKudosu(TestCase):
    def test_deserialize(self):
        api.user_kudosu(user_id=3178418)

class TestBeatmapScores(TestCase):
    def test_deserialize(self):
        api.beatmap_scores(beatmap_id=1981090)

class TestBeatmap(TestCase):
    def test_deserialize(self):
        api.beatmap(beatmap_id=221777)

class TestBeatmapset(TestCase):
    def test_deserialize(self):
        api.beatmapset(beatmap_id=3207950)

class TestBeatmapsetEvents(TestCase):
    def test_deserialize(self):
        api.beatmapset_events()

    def test_all_types(self):
        # beatmapset_events is a really complicated endpoint in terms of return
        # types. We want to make sure both that we're not doing anything wrong,
        # and the osu! api isn't doing anything wrong by returning something
        # that doesn't match their documentation.
        for event_type in BeatmapsetEventType:
            api.beatmapset_events(types=[event_type])

class TestRanking(TestCase):
    def test_deserialize(self):
        api.ranking("osu", RankingType.PERFORMANCE, country="US")

class TestUserScores(TestCase):
    def test_deserialize(self):
        api.user_scores(12092800, "best")

class TestBeatmapUserScore(TestCase):
    def test_deserialize(self):
        api.beatmap_user_score(beatmap_id=221777, user_id=2757689, mode="osu")

class TestSearch(TestCase):
    def test_deserialize(self):
        api.search(query="peppy")

class TestComment(TestCase):
    def test_deserialize(self):
        api.comment(comment_id=1)

class TestDownloadScore(TestCase):
    def test_deserialize(self):
        # api instance is using client credentials which doesn't have access to
        # downloading replays
        self.assertRaises(AccessDeniedError,
            lambda: api.download_score(mode="osu", score_id=2797309065))

class TestSearchBeatmaps(TestCase):
    def test_deserialize(self):
        api.search_beatmapsets(query="the big black")

class TestUser(TestCase):
    def test_deserialize(self):
        api.user(12092800)

    def test_key(self):
        # make sure it automatically falls back to username if not specified
        api.user("tybug2")
        api.user("tybug2", key="username")

        self.assertRaises(Exception, lambda: api.user("tybug2", key="id"))

class TestMe(TestCase):
    def test_deserialize(self):
        # requires an authorization code api for the identify scope, client
        # credentials can only request the public scope
        self.assertRaises(InsufficientScopeError, api.get_me)

class TestWikiPage(TestCase):
    def test_deserialize(self):
        api.wiki_page("en", "Welcome")

class TestChangelogBuild(TestCase):
    def test_deserialize(self):
        api.changelog_build("stable40", "20210520.2")

class TestChangelogListing(TestCase):
    def test_deserialize(self):
        api.changelog_listing()

class TestChangelogLookup(TestCase):
    def test_deserialize(self):
        api.changelog_lookup("lazer")

class TestForumTopic(TestCase):
    def test_deserialize(self):
        api.forum_topic(141240)

class TestBeatmapsetDiscussionVotes(TestCase):
    def test_deserialize(self):
        api.beatmapset_discussion_votes().votes[0].score

class TestBeatmapsetDiscussions(TestCase):
    def test_deserialize(self):
        api.beatmapset_discussions()

class TestNewsListing(TestCase):
    def test_deserialize(self):
        # Target ID of 2070907 is Tillerino
        self.api = OssapiV2(
            client_id, client_secret, redirect_uri="http://localhost:9409/",
            scopes=["chat.write"], strict=True,
            token_file_override=(Path(__file__).parent / "authorization_code_TestCreateNewPM.pickle")
        )
        self.api.create_pm(user_id=2070907, message="Integration test please ignore")

class TestForumWriteMethods(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = OssapiV2(
            dev_client_id, dev_client_secret, redirect_uri="http://localhost:9409/",
            scopes=["forum.write"], strict=True, osu_host=DEV_HOST,
            token_file_override=(Path(__file__).parent / "authorization_code_TestForumWriteMethods.pickle")
        )

    def test_create_topic(self):
        try:
            self.api.create_forum_topic(
                body="Integration test please ignore",
                forum_id=74,
                title="Integration test please ignore",
            )
        except ValueError as ex:
            if "Editing beatmap metadata post is not allowed." in str(ex):
                self.fail("Encountered unexpected error message")

    # TODO: Figure out why polls aren't working :)
    @unittest.skip
    def test_create_with_poll(self):
        poll = {
            "options": ["Option 1", "Option 2"],
            "title": "Test Poll",
            "length_days": 0,
            "vote_change": True,
            "max_options": 1,
        }
        self.api.create_forum_topic(
            **{
                "body": "Integration test with poll - please ignore" + str(datetime.now()),
                "forum_id": 78,
                "title": "Integration test with poll - please ignore" + str(datetime.now()),
                "with_poll": True,
                "poll": poll,
            }
        )

    def test_reply_topic(self):
        try:
            self.api.reply_to_forum_topic(
                topic_id=156,
                body="Integration test reply please ignore " + str(datetime.now()),
            )
        except ValueError as ex:
            if "Please edit your last post instead of posting again." not in str(ex):
                self.fail("Encountered unexpected error message")

    def test_edit_topic(self):
        self.api.edit_forum_topic(
            topic_id=156,
            title="Title last updated: " + str(datetime.now()),
        )

    def test_edit_post(self):
        self.api.edit_forum_post(
            body="This comment was last edited at: " + str(datetime.now()),
            post_id=306,
        )
        api.news_listing(year=2021)

class TestNewsPost(TestCase):
    def test_deserialize(self):
        api.news_post(1025, key="id")

class TestSeasonalBackgrounds(TestCase):
    def test_deserialize(self):
        api.seasonal_backgrounds()


# TODO requires friends.read scope
# class TestFriends(TestCase):
#     def test_deserialize(self):
#         api.friends()

# TODO requires chat.write scope
# class TestCreateNewPM(TestCase):
#     def test_deserialize(self):
#         api.create_pm(2070907, "Unit test from ossapi "
#             "(https://github.com/circleguard/ossapi/), please ignore")
