[![PyPI version](https://badge.fury.io/py/ossapi.svg)](https://pypi.org/project/ossapi/)

# ossapi ([documentation](https://circleguard.github.io/ossapi/))

ossapi is a python wrapper for the osu! api. ossapi supports both [api v2](https://osu.ppy.sh/docs/index.html) and [api v1](https://github.com/ppy/osu-api/wiki) and has every endpoint in both implemented.

To install:

```bash
pip install ossapi
```

To upgrade:

```bash
pip install -U ossapi
```

To get started, read the docs: https://circleguard.github.io/ossapi/.

If you need support or would like to contribute, feel free to join the circleguard discord: <https://discord.gg/e84qxkQ>.

## Quickstart

[The docs](https://circleguard.github.io/ossapi/) have an [in depth quickstart](https://circleguard.github.io/ossapi/creating-a-client.html), but here's a super short version:

```python
from ossapi import Ossapi
# create a new client at https://osu.ppy.sh/home/account/edit#oauth
client_id = None
client_secret = None
callback_url = None # choose a port on localhost, eg http://localhost:727/

# client credentials authentication...
api = Ossapi(client_id, client_secret)

# ...or authorization grant authentication
api = Ossapi(client_id, client_secret, callback_url)

# go wild with endpoint calls! See docs for all endpoints
print(api.user("tybug2"))
```

### Advanced Usage

#### Models as Parameters

As a convenience, you can pass a `User`, `Beatmap`, or `Beatmapset` to any function in place of a `user_id`, `beatmap_id`, or `beatmapset_id` respectively. For instance:

```python
beatmap = api.beatmap(221777)
assert api.beatmap_scores(beatmap) == api.beatmap_scores(221777)
```

## API v1 Usage

You can get your api v1 key at <https://osu.ppy.sh/p/api/>. Note that due to a [redirection bug](https://github.com/ppy/osu-web/issues/2867), you may need to log in and wait 30 seconds before being able to access the api page through the above link.

Basic usage:

```python
from ossapi import Ossapi

api = Ossapi("key")
print(api.get_beatmaps(user=53378)[0].submit_date)
print(api.get_match(69063884).games[0].game_id)
print(api.get_scores(221777)[0].username)
print(len(api.get_replay(beatmap_id=221777, user=6974470)))
print(api.get_user(12092800).playcount)
print(api.get_user_best(12092800)[0].pp)
print(api.get_user_recent(12092800)[0].beatmap_id)
```

For convenience when working with mods, we provide a Mod class, which is used wherever the api returns a mod value. An overview of its methods, in example format:

```python
from ossapi import Mod, Ossapi

api = Ossapi("key")

mods = api.get_scores(221777)[0].mods
# Mod's __str__ uses short_name()
print(mods)
print(mods.short_name())

# to break down a mod into its component mods (eg if you want ["HD", "DT"] from "HDDT")
print(mods.decompose())

# to get the long form name (HD -> Hidden)
print(mods.long_name())

# to access the underlying value
print(mods.value)

# to add or remove a mod from the mod combination, use + and -
print(mods + Mod.FL)
print(mods - Mod.HD)
# you can also add or remove multiple mods at a time
print(mods - Mod.HDHR)

# common mod combinations are stored as static variables under `Mod` for convenience
print(Mod.HDDT, Mod.HDHR, Mod.HDDTHR)
# otherwise, the preferred way to build up mods is by adding them together
print(Mod.HD + Mod.FL + Mod.EZ)
# alternatively, you can instantiate with the raw value
print(Mod(1034))
assert Mod.HD + Mod.FL + Mod.EZ == Mod(1034)
```
