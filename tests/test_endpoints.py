from datetime import datetime
from unittest import TestCase

from ossapi import (RankingType, BeatmapsetEventType, AccessDeniedError,
    InsufficientScopeError, Mod, GameMode, NewsPostKey)

from tests import (api_v2, api_v2_full, api_v2_dev, TestCaseAuthorizationCode,
    TestCaseDevServer)

class TestBeatmapsetDiscussionPosts(TestCase):
    def test_deserialize(self):
        api_v2.beatmapset_discussion_posts()

class TestUserRecentActivity(TestCase):
    def test_deserialize(self):
        api_v2.user_recent_activity(12092800)

class TestSpotlights(TestCase):
    def test_deserialize(self):
        api_v2.spotlights()

class TestUserBeatmaps(TestCase):
    def test_deserialize(self):
        api_v2.user_beatmaps(user_id=12092800, type_="most_played")

class TestUserKudosu(TestCase):
    def test_deserialize(self):
        api_v2.user_kudosu(user_id=3178418)

class TestBeatmapScores(TestCase):
    def test_deserialize(self):
        api_v2.beatmap_scores(beatmap_id=1981090)

class TestBeatmap(TestCase):
    def test_deserialize(self):
        api_v2.beatmap(beatmap_id=221777)

        # beatmap with a diff owner
        bm = api_v2.beatmap(beatmap_id=1604098)
        # might need to be updated when
        # https://github.com/ppy/osu-web/issues/9784 is addressed.
        self.assertIsNone(bm.owner)

class TestBeatmapset(TestCase):
    def test_deserialize(self):
        api_v2.beatmapset(beatmap_id=3207950)

class TestBeatmapsetEvents(TestCase):
    def test_deserialize(self):
        api_v2.beatmapset_events()

    def test_all_types(self):
        # beatmapset_events is a really complicated endpoint in terms of return
        # types. We want to make sure both that we're not doing anything wrong,
        # and the osu! api isn't doing anything wrong by returning something
        # that doesn't match their documentation.
        for event_type in BeatmapsetEventType:
            api_v2.beatmapset_events(types=[event_type])

class TestRanking(TestCase):
    def test_deserialize(self):
        api_v2.ranking("osu", RankingType.PERFORMANCE, country="US")

class TestUserScores(TestCase):
    def test_deserialize(self):
        api_v2.user_scores(12092800, "best")

class TestBeatmapUserScore(TestCase):
    def test_deserialize(self):
        api_v2.beatmap_user_score(beatmap_id=221777, user_id=2757689, mode="osu")

class TestBeatmapUserScores(TestCase):
    def test_deserialize(self):
        api_v2.beatmap_user_scores(beatmap_id=221777, user_id=2757689, mode="osu")

class TestSearch(TestCase):
    def test_deserialize(self):
        api_v2.search(query="peppy")

class TestComment(TestCase):
    def test_deserialize(self):
        api_v2.comment(comment_id=1)

class TestSearchBeatmaps(TestCase):
    def test_deserialize(self):
        api_v2.search_beatmapsets(query="the big black")

class TestUser(TestCase):
    def test_deserialize(self):
        api_v2.user(12092800)

    def test_key(self):
        # make sure it automatically falls back to username if not specified
        api_v2.user("tybug2")
        api_v2.user("tybug2", key="username")

        self.assertRaises(Exception, lambda: api_v2.user("tybug2", key="id"))

class TestWikiPage(TestCase):
    def test_deserialize(self):
        api_v2.wiki_page("en", "Welcome")

class TestChangelogBuild(TestCase):
    def test_deserialize(self):
        api_v2.changelog_build("stable40", "20210520.2")

class TestChangelogListing(TestCase):
    def test_deserialize(self):
        api_v2.changelog_listing()

class TestChangelogLookup(TestCase):
    def test_deserialize(self):
        api_v2.changelog_lookup("lazer")

class TestForumTopic(TestCase):
    def test_deserialize(self):
        api_v2.forum_topic(141240)

class TestBeatmapsetDiscussionVotes(TestCase):
    def test_deserialize(self):
        api_v2.beatmapset_discussion_votes().votes[0].score

class TestBeatmapsetDiscussions(TestCase):
    def test_deserialize(self):
        api_v2.beatmapset_discussions()

class TestNewsPost(TestCase):
    def test_deserialize(self):
        api_v2.news_post(1025, key=NewsPostKey.ID)

class TestSeasonalBackgrounds(TestCase):
    def test_deserialize(self):
        api_v2.seasonal_backgrounds()



# ======================
# api_v2_full test cases
# ======================

class TestCreateNewPM(TestCaseAuthorizationCode):
    def test_deserialize(self):
        # tillerino
        api_v2_full.send_pm(2070907, "Unit test from ossapi "
            "(https://github.com/circleguard/ossapi/), please ignore")

class TestDownloadScore(TestCaseAuthorizationCode):
    def test_access_denied(self):
        # make sure client credentials api (`api`) can't access this endpoint
        self.assertRaises(AccessDeniedError,
            lambda: api_v2.download_score(mode="osu", score_id=2797309065))

    def test_deserialize(self):
        # but the authorization code api (`api_v2_full`) can
        api_v2_full.download_score(mode="osu", score_id=2797309065)

class TestBeatmapAttributes(TestCase):
    def test_deserialize(self):
        api_v2.beatmap_attributes(221777, ruleset="osu")
        api_v2.beatmap_attributes(221777, mods=Mod.HDDT)
        api_v2.beatmap_attributes(221777, mods="HR")
        api_v2.beatmap_attributes(221777, ruleset_id=0)

class TestUsers(TestCase):
    def test_deserialize(self):
        api_v2.users([12092800])

class TestBeatmaps(TestCase):
    def test_deserialize(self):
        api_v2.beatmaps([221777])

class TestScore(TestCase):
    def test_deserialize(self):
        # downloadable
        api_v2.score(GameMode.OSU, 2243145877)
        # downloadable, my score
        api_v2.score(GameMode.OSU, 3685255338)
        # not downloadable, my score
        api_v2.score(GameMode.OSU, 3772000814)

        # other gamemodes
        api_v2.score(GameMode.TAIKO, 176904666)
        api_v2.score(GameMode.MANIA, 524674141)
        api_v2.score(GameMode.CATCH, 211167989)

class TestMe(TestCaseAuthorizationCode):
    def test_insufficient_scope(self):
        # client credentials api can't request `Scope.IDENTIFY` and so can't
        # access /me
        self.assertRaises(InsufficientScopeError, api_v2.get_me)

    def test_deserialize(self):
        # but the authorization code api can
        api_v2_full.get_me()

class TestFriends(TestCaseAuthorizationCode):
    def test_access_denied(self):
        self.assertRaises(InsufficientScopeError, api_v2.friends)

    def test_deserialize(self):
        api_v2_full.friends()

# =====================
# api_v2_dev test cases
# =====================

class TestForumCreateTopic(TestCaseDevServer):
    def test_create(self):
        api_v2_dev.forum_create_topic("Integration test please ignore",
            74, "Integration test please ignore")

    def test_create_with_poll(self):
        poll = {
            "options": ["Option 1", "Option 2"],
            "title": "Test Poll",
            "length_days": 0,
            "vote_change": True,
            "max_options": 1,
        }
        api_v2_dev.forum_create_topic(body="Integration test with poll - please ignore" + str(datetime.now()),
            forum_id=78,
            title="Integration test with poll - please ignore" + str(datetime.now()),
            with_poll=True, poll=poll)

class TestForumReply(TestCaseDevServer):
    def test_reply(self):
        api_v2_dev.forum_reply(156, "unit test from ossapi "
            "(https://github.com/circleguard/ossapi/), please ignore")

# TODO first create a topic, then try and edit that one (this will fail if it's
# not our topic id)

class TestForumEditTopic(TestCaseDevServer):
    def test_edit(self):
        api_v2_dev.forum_edit_topic(156, f"Title last updated at {datetime.now()}")

class TestForumEditPost(TestCaseDevServer):
    def test_edit(self):
        api_v2_dev.forum_edit_post(306,
            f"This comment was last edited at {datetime.now()}")
