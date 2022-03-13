from dataIO import fileIO
import os

false_strings = ["false", "False", "f", "F", "0", ""]

if fileIO("config.json", "check"):
    config = fileIO("config.json", "load")
else:
    config = {
        "lucha_floor_token_id": os.environ["LUCHA_FLOOR_TOKEN_ID"],
        "lucha_icon_url": os.environ["LUCHA_ICON_URL"],
        "opensea_api_key": os.environ["OPENSEA_API_KEY"],
        "embedded_description_floors": os.environ["EMBEDDED_DESCRIPTION_FLOORS"],
        "embedded_description_stats": os.environ["EMBEDDED_DESCRIPTION_STATS"],
        "discord_channel_id": os.environ["DISCORD_CHANNEL_ID"],
        "database_url": os.environ["DATABASE_URL"],
        "money_visual": os.environ["MONEY_VISUAL"],
        "slug_used": os.environ["SLUG_USED"],
        "bot_name_prefix": os.environ["BOT_NAME_PREFIX"],
        "embed_title_lucha_floors": os.environ["EMBED_TITLE_LUCHA_FLOORS"],
        "embed_title_lucha_stats" : os.environ["EMBED_TITLE_LUCHA_STATS"],
        "hidden_mustache_code" : os.environ["HIDDEN_MUSTACHE_CODE"],
        "dune_login" : os.environ["DUNE_LOGIN"],
        "dune_pwd" : os.environ["DUNE_PWD"],
        "dune_query_hidden_mustache_ids" : os.environ["DUNE_QUERY_HIDDEN_MUSTACHE_IDS"],
        "opensea_assets_contract_address" : os.environ["OPENSEA_ASSETS_CONTRACT_ADDRESS"]
    }