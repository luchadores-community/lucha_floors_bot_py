import requests
import json
from config import config
from bs4 import BeautifulSoup
from opensea import OpenseaAPI
from luchaDune import DuneQuerries

class OpenseaQuerries:

    async def find_a_floor_per_attr(nbAttr):
        print("-- request for " + str(nbAttr) + "T")
        headers = {
            #'X-API-KEY':str(config['opensea_api_key']),
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0'
        }
        opensea_url = "https://opensea.io/collection/luchadores-io?search[numericTraits][0][name]=Attributes&search[numericTraits][0][ranges][0][max]="+nbAttr+"&search[numericTraits][0][ranges][0][min]="+nbAttr+"&search[sortAscending]=true&search[sortBy]=PRICE&search[toggles][0]=BUY_NOW"
        
        resp = requests.get(url=opensea_url, headers=headers)
        if resp.status_code != 200:
            print("Error. status_code=" + str(resp.status_code))
            return
        bswebpage = BeautifulSoup(resp.text, "html.parser")
        
        for assetCardFooter in bswebpage.findAll('div',{'class':'sc-1xf18x6-0 sc-1twd32i-0 sc-1wwz3hp-0 xGokL kKpYwv kuGBEl'}):
            floor = assetCardFooter.findAll('div', {'class':'Price--amount'})[0].text.strip()
            print("-- floor = " + floor)
            return floor

    async def get_collection_stats(slug):
        headers = {
                "Accept": "application/json",
                #"X-API-KEY": str(config['opensea_api_key']),
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0"
        }

        url = "https://api.opensea.io/api/v1/collection/"+slug+"/stats"    
        resp = requests.request("GET", url, headers=headers)
        return resp.json()
        #api = OpenseaAPI(apikey=str(config['opensea_api_key']))
        #return api.collection_stats(collection_slug=slug)

    async def get_hidden_mustache_floor():
        prices = []
        ids = await DuneQuerries.get_hidden_ids()
        if len(ids) > 0:
            split_ids = [ids[i * 20:(i + 1) * 20] for i in range((len(ids) + 20 - 1) // 20 )]

            headers = {
                "Accept": "application/json",
                #"X-API-KEY": str(config['opensea_api_key']),
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0"
            }
            
            for batch_ids in split_ids:
                formatIds = ""
                for id in batch_ids:
                    formatIds = formatIds + "&token_ids=" + str(id)
                url = "https://api.opensea.io/wyvern/v1/orders?asset_contract_address="+str(config["opensea_assets_contract_address"])+"&bundled=false&include_bundled=false"+formatIds+"&side=1&sale_kind=0&limit=50&offset=0&order_by=created_date&order_direction=desc"    
                resp = requests.request("GET", url, headers=headers)
                if resp.status_code != 200:
                    print("Error. status_code=" + str(resp.status_code))
                    return
                respDict = json.loads(resp.text)
                for order in respDict['orders']:
                    prices.append(order['current_price'])

        return OpenseaQuerries._get_floor(prices)

    def _get_floor(prices):
        floor = 0
        for p_wei in prices:
            p_eth = round(float(p_wei)*10e-19, 2)
            if floor == 0:
                floor = p_eth
            elif p_eth < floor:
                floor = p_eth
        return floor
    

