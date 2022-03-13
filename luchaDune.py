from duneanalytics import DuneAnalytics
from config import config

class DuneQuerries:

    async def get_hidden_ids():
        dune = DuneAnalytics(str(config["dune_login"]), str(config["dune_pwd"]))
        dune.login()
        dune.fetch_auth_token()
        result_id = dune.query_result_id(query_id=int(config["dune_query_hidden_mustache_ids"]))
        data = dune.query_result(result_id)
        hidden_mustache_ids = []
        if len(data['data']['get_result_by_result_id']) > 0:
            for found in data['data']['get_result_by_result_id']:
                hidden_mustache_ids.append(found['data']['id'])  
        else:
            print("Error, no hidden mustache ids found")
        return hidden_mustache_ids

