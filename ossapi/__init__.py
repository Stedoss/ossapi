import logging
# we need to explicitly set a handler for the logging module to be happy
handler = logging.StreamHandler()
logging.getLogger("ossapi").addHandler(handler)

from ossapi.ossapi import (Ossapi, ReplayUnavailableException,
    InvalidKeyException, APIException)
from ossapi.ossapiv2 import OssapiV2, Grant, Scope
from ossapi.models import (Beatmap, BeatmapCompact, BeatmapUserScore,
    ForumTopicAndPosts, Search, CommentBundle, Cursor, Score,
    BeatmapsetSearchResult, ModdingHistoryEventsBundle, User, Rankings,
    BeatmapScores, KudosuHistory, Beatmapset, BeatmapPlaycount, Spotlight,
    Spotlights, WikiPage, _Event, Event, BeatmapsetDiscussionPosts, Build,
    ChangelogListing, MultiplayerScores, MultiplayerScoresCursor,
    BeatmapsetDiscussionVotes, CreatePMResponse, BeatmapsetDiscussions,
    UserCompact, BeatmapsetCompact, ForumPoll, Room, RoomPlaylistItem,
    RoomPlaylistItemMod, RoomLeaderboardScore, RoomLeaderboardUserScore,
    RoomLeaderboard)
from ossapi.enums import (GameMode, ScoreType, RankingFilter, RankingType,
    UserBeatmapType, BeatmapDiscussionPostSort, UserLookupKey,
    BeatmapsetEventType, CommentableType, CommentSort, ForumTopicSort,
    SearchMode, MultiplayerScoresSort, BeatmapsetDiscussionVote,
    BeatmapsetDiscussionVoteSort, BeatmapsetStatus, MessageType,
    BeatmapsetSearchCategory, BeatmapsetSearchMode,
    BeatmapsetSearchExplicitContent, BeatmapsetSearchLanguage,
    BeatmapsetSearchGenre, NewsPostKey, BeatmapsetSearchSort, RoomType,
    RoomCategory)
from ossapi.mod import Mod
from ossapi.replay import Replay
from ossapi.version import __version__
from ossapi.encoder import ModelEncoder, serialize_model

from oauthlib.oauth2 import AccessDeniedError, TokenExpiredError
from oauthlib.oauth2.rfc6749.errors import InsufficientScopeError


__all__ = [
    # OssapiV1
    "Ossapi", "ReplayUnavailableException", "InvalidKeyException",
    "APIException",
    # OssapiV2 core
    "OssapiV2", "Grant", "Scope",
    # OssapiV2 models
    "Beatmap", "BeatmapCompact", "BeatmapUserScore", "ForumTopicAndPosts",
    "Search", "CommentBundle", "Cursor", "Score", "BeatmapsetSearchResult",
    "ModdingHistoryEventsBundle", "User", "Rankings", "BeatmapScores",
    "KudosuHistory", "Beatmapset", "BeatmapPlaycount", "Spotlight",
    "Spotlights", "WikiPage", "_Event", "Event", "BeatmapsetDiscussionPosts",
    "Build", "ChangelogListing", "MultiplayerScores", "MultiplayerScoresCursor",
    "BeatmapsetDiscussionVotes", "CreatePMResponse",
    "BeatmapsetDiscussions", "UserCompact", "BeatmapsetCompact", "ForumPoll",
    "Room", "RoomPlaylistItem", "RoomPlaylistItemMod", "RoomLeaderboardScore",
    "RoomLeaderboardUserScore", "RoomLeaderboard",
    # OssapiV2 enums
    "GameMode", "ScoreType", "RankingFilter", "RankingType",
    "UserBeatmapType", "BeatmapDiscussionPostSort", "UserLookupKey",
    "BeatmapsetEventType", "CommentableType", "CommentSort", "ForumTopicSort",
    "SearchMode", "MultiplayerScoresSort", "BeatmapsetDiscussionVote",
    "BeatmapsetDiscussionVoteSort", "BeatmapsetStatus", "MessageType",
    "BeatmapsetSearchCategory", "BeatmapsetSearchMode",
    "BeatmapsetSearchExplicitContent", "BeatmapsetSearchLanguage",
    "BeatmapsetSearchGenre", "NewsPostKey", "BeatmapsetSearchSort", "RoomType",
    "RoomCategory",
    # OssapiV2 exceptions
    "AccessDeniedError", "TokenExpiredError", "InsufficientScopeError",
    # misc
    "Mod", "Replay", "__version__", "ModelEncoder",
    "serialize_model"
]
