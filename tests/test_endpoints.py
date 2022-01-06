import unittest
from datetime import datetime
from unittest import TestCase

from ossapi import (RankingType, BeatmapsetEventType, AccessDeniedError,
    InsufficientScopeError, NewsPostKey)

from tests import api, api_full, api_dev

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

class TestNewsPost(TestCase):
    def test_deserialize(self):
        api.news_post(1025, key=NewsPostKey.ID)

class TestSeasonalBackgrounds(TestCase):
    def test_deserialize(self):
        api.seasonal_backgrounds()

class TestFriends(TestCase):
    def test_deserialize(self):
        api.friends()



# ===================
# api_full test cases
# ===================

class TestCreateNewPM(TestCase):
    def test_deserialize(self):
        # tillerino
        api_full.send_pm(2070907, "Unit test from ossapi "
            "(https://github.com/circleguard/ossapi/), please ignore")



# ==================
# api_dev test cases
# ==================

class TestForumCreateTopic(TestCase):
    def test_create(self):
        try:
            api_dev.forum_create_topic("Integration test please ignore",
                74, "Integration test please ignore")
        except ValueError as ex:
            if "Editing beatmap metadata post is not allowed." in str(ex):
                self.fail("Encountered unexpected error message")

    def test_create_with_poll(self):
        poll = {
            "options": ["Option 1", "Option 2"],
            "title": "Test Poll",
            "length_days": 0,
            "vote_change": True,
            "max_options": 1,
        }
        api_dev.forum_create_topic(body="Integration test with poll - please ignore" + str(datetime.now()),
            forum_id=78,
            title="Integration test with poll - please ignore" + str(datetime.now()),
            with_poll=True, poll=poll)

class TestForumReply(TestCase):
    def test_reply(self):
        try:
            api_dev.forum_reply(156, "unit test from ossapi "
                "(https://github.com/circleguard/ossapi/), please ignore")
        except ValueError as ex:
            if "Please edit your last post instead of posting again." not in str(ex):
                self.fail("Encountered unexpected error message")

class TestForumEditTopic(TestCase):
    def test_edit(self):
        api_dev.forum_edit_topic(156, f"Title last updated at {datetime.now()}")

class TestForumEditPost(TestCase):
    def test_edit(self):
        api_dev.forum_edit_post(306,
            f"This comment was last edited at {datetime.now()}")
