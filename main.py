from datetime import datetime

from discord import Embed, Activity, ActivityType, Forbidden
from discord.ext import commands, tasks

from config import config
from luchaOpensea import OpenseaQuerries

luchaFloors = commands.Bot(command_prefix = "!", description = "LuchaFloors")

@luchaFloors.event
async def on_ready():
    print('LuchaFloors ready !')
    update_task.start()

@tasks.loop(minutes=11.0)
async def update_task():
    await luchaFloors.change_presence(activity=Activity(type=ActivityType.watching, name="Refreshing..."))
    await Processors.update_bot()
    await luchaFloors.change_presence(activity=Activity(type=ActivityType.watching, name="Luchadores floors"))

class Processors:

    async def update_bot():
        print(str(datetime.utcnow()) + ': update_bot')
        if luchaFloors.is_ready:
            await Processors._update_stats_data()
            await Processors._update_embedded_floors()   

    async def _update_stats_data():
        stats = await OpenseaQuerries.get_collection_stats(str(config["slug_used"]))
        await Processors._update_bot_status(stats)
        await Processors._update_embedded_stats(stats)

    async def _update_bot_status(stats):
        print(str(datetime.utcnow()) + ': update_bot_status')
        for guild in luchaFloors.guilds:
            try:
                await guild.me.edit(nick=str(config["bot_name_prefix"]) + str(stats["stats"]["floor_price"]) + str(config["money_visual"]))
            except Forbidden as ex:
                print("Error : bot don't have permission to update nick in guild " + str(guild.name))        

    async def _update_embedded_floors():
        print(str(datetime.utcnow()) + ': update_embedded_floors')
        messageToUpdate = await Processors._get_bot_pinned_messages(str(config["embed_title_lucha_floors"]))
        await messageToUpdate.edit(embed=await Processors._get_embedded_floors())
        if messageToUpdate.content == "--init--":
            await messageToUpdate.edit(content="")

    async def _update_embedded_stats(stats):
        print(str(datetime.utcnow()) + ': _update_embedded_stats')
        messageToUpdate = await Processors._get_bot_pinned_messages(str(config["embed_title_lucha_stats"]))
        await messageToUpdate.edit(embed=await Processors._get_embedded_stats(stats))
        if messageToUpdate.content == "--init--":
            await messageToUpdate.edit(content="")

    async def _get_bot_pinned_messages(title):
        channel = luchaFloors.get_channel(int(config["discord_channel_id"]))
        pins = await channel.pins()
        for pin in pins:
            if pin.author == luchaFloors.user:
                if len(pin.embeds) > 0 and pin.embeds[0].title == str(title):
                    return pin
        sentMessage = await channel.send(content="--init--")
        await sentMessage.pin()
        return sentMessage
    
    async def _get_embedded_floors():
        embed = Embed(title=str(config["embed_title_lucha_floors"]), description=config["embedded_description_floors"], colour=0x87CEEB, timestamp=datetime.utcnow())
        i = 0
        while i < 8:
            embed.add_field(name=str(i) + "T", value=str(await OpenseaQuerries.find_a_floor_per_attr(str(i))) + str(config["money_visual"]), inline=False)
            i = i + 1
        #embed.add_field(name=str(config["hidden_mustache_code"]), value=str(await OpenseaQuerries.get_hidden_mustache_floor()) + str(config["money_visual"]), inline=False)
        embed.set_footer(text="luchadores.io", icon_url=config["lucha_icon_url"])
        return embed
    
    async def _get_embedded_stats(stats):
        embed = Embed(title=str(config["embed_title_lucha_stats"]), description=config["embedded_description_stats"], colour=0x87CEEB, timestamp=datetime.utcnow())

        statsLuchadores = await OpenseaQuerries.get_collection_stats(str(config["slug_used"]))
        statsPinatas = await OpenseaQuerries.get_collection_stats("luchadores-io-pinatas")
        statsWearables = await OpenseaQuerries.get_collection_stats("luchadores-io-wearables")

        embed.add_field(name='\u200B', inline=False, value='<:luchador:922912148013846550>')
        embed.add_field(name="7 days", inline=True, value=
            "Volume: " + str(round(statsLuchadores['stats']['seven_day_volume'], 2)) + str(config["money_visual"]) + '\r' +
            "Change: " + str(round(statsLuchadores['stats']['seven_day_change'], 2)) + str(config["money_visual"]) + '\r' +
            "Sales: " + str(round(statsLuchadores['stats']['seven_day_sales'])) + '\r' +
            "Average price: " + str(round(statsLuchadores['stats']['seven_day_average_price'], 2)) + str(config["money_visual"]) + '\r')
        embed.add_field(name="30 days", inline=True, value=
            "Volume: " + str(round(statsLuchadores['stats']['thirty_day_volume'], 2)) + str(config["money_visual"]) + '\r' +
            "Change: " + str(round(statsLuchadores['stats']['thirty_day_change'], 2)) + str(config["money_visual"]) + '\r' +
            "Sales: " + str(round(statsLuchadores['stats']['thirty_day_sales'])) + '\r' +
            "Average price: " + str(round(statsLuchadores['stats']['thirty_day_average_price'], 2)) + str(config["money_visual"]) + '\r')
        embed.add_field(name="All time", inline=True, value=
            "Volume: " + str(round(statsLuchadores['stats']['total_volume'], 2)) + str(config["money_visual"]) + '\r' +
            "Sales: " + str(round(statsLuchadores['stats']['total_sales'])) + '\r')
        
        embed.add_field(name='\u200B', inline=False, value='<:cometh_titan:936284027634221058>')
        embed.add_field(name="7 days", inline=True, value=
            "Volume: " + str(round(statsWearables['stats']['seven_day_volume'], 2)) + str(config["money_visual"]) + '\r' +
            "Change: " + str(round(statsWearables['stats']['seven_day_change'], 2)) + str(config["money_visual"]) + '\r' +
            "Sales: " + str(round(statsWearables['stats']['seven_day_sales'])) + '\r' +
            "Average price: " + str(round(statsWearables['stats']['seven_day_average_price'], 2)) + str(config["money_visual"]) + '\r')
        embed.add_field(name="30 days", inline=True, value=
            "Volume: " + str(round(statsWearables['stats']['thirty_day_volume'], 2)) + str(config["money_visual"]) + '\r' +
            "Change: " + str(round(statsWearables['stats']['thirty_day_change'], 2)) + str(config["money_visual"]) + '\r' +
            "Sales: " + str(round(statsWearables['stats']['thirty_day_sales'])) + '\r' +
            "Average price: " + str(round(statsWearables['stats']['thirty_day_average_price'], 2)) + str(config["money_visual"]) + '\r')
        embed.add_field(name="All time", inline=True, value=
            "Volume: " + str(round(statsWearables['stats']['total_volume'], 2)) + str(config["money_visual"]) + '\r' +
            "Sales: " + str(round(statsWearables['stats']['total_sales'])) + '\r')

        embed.add_field(name='\u200B', inline=False, value='<:lucha_pinata:933304310610165800>')
        embed.add_field(name="7 days", inline=True, value=
            "Volume: " + str(round(statsPinatas['stats']['seven_day_volume'], 2)) + str(config["money_visual"]) + '\r' +
            "Change: " + str(round(statsPinatas['stats']['seven_day_change'], 2)) + str(config["money_visual"]) + '\r' +
            "Sales: " + str(round(statsPinatas['stats']['seven_day_sales'])) + '\r' +
            "Average price: " + str(round(statsPinatas['stats']['seven_day_average_price'], 2)) + str(config["money_visual"]) + '\r')
        embed.add_field(name="30 days", inline=True, value=
            "Volume: " + str(round(statsPinatas['stats']['thirty_day_volume'], 2)) + str(config["money_visual"]) + '\r' +
            "Change: " + str(round(statsPinatas['stats']['thirty_day_change'], 2)) + str(config["money_visual"]) + '\r' +
            "Sales: " + str(round(statsPinatas['stats']['thirty_day_sales'])) + '\r' +
            "Average price: " + str(round(statsPinatas['stats']['thirty_day_average_price'], 2)) + str(config["money_visual"]) + '\r')
        embed.add_field(name="All time", inline=True, value=
            "Volume: " + str(round(statsPinatas['stats']['total_volume'], 2)) + str(config["money_visual"]) + '\r' +
            "Sales: " + str(round(statsPinatas['stats']['total_sales'])) + '\r')
        
        embed.add_field(name='\u200B', inline=False, value='<:luchador:922912148013846550> + <:cometh_titan:936284027634221058> + <:lucha_pinata:933304310610165800>')
        embed.add_field(name="7 days", inline=True, value=
            "Volume: " + str(round(statsLuchadores['stats']['seven_day_volume'] + statsPinatas['stats']['seven_day_volume'] + statsWearables['stats']['seven_day_volume'], 2)) + str(config["money_visual"]) + '\r' +
            "Change: " + str(round(statsLuchadores['stats']['seven_day_change'] + statsPinatas['stats']['seven_day_change'] + statsWearables['stats']['seven_day_change'], 2)) + str(config["money_visual"]) + '\r' +
            "Sales: " + str(round(statsLuchadores['stats']['seven_day_sales'] + statsPinatas['stats']['seven_day_sales'] + statsWearables['stats']['seven_day_sales'])) + '\r' +
            "Average price: " + str(round(statsLuchadores['stats']['seven_day_average_price'] + statsPinatas['stats']['seven_day_average_price'] + statsWearables['stats']['seven_day_average_price'], 2)) + str(config["money_visual"]) + '\r')
        embed.add_field(name="30 days", inline=True, value=
            "Volume: " + str(round(statsLuchadores['stats']['thirty_day_volume'] + statsPinatas['stats']['thirty_day_volume'] + statsWearables['stats']['thirty_day_volume'], 2)) + str(config["money_visual"]) + '\r' +
            "Change: " + str(round(statsLuchadores['stats']['thirty_day_change'] + statsPinatas['stats']['thirty_day_change'] + statsWearables['stats']['thirty_day_change'], 2)) + str(config["money_visual"]) + '\r' +
            "Sales: " + str(round(statsLuchadores['stats']['thirty_day_sales'] + statsPinatas['stats']['thirty_day_sales'] + statsWearables['stats']['thirty_day_sales'])) + '\r' +
            "Average price: " + str(round(statsLuchadores['stats']['thirty_day_average_price'] + statsPinatas['stats']['thirty_day_average_price'] + statsWearables['stats']['thirty_day_average_price'], 2)) + str(config["money_visual"]) + '\r')
        embed.add_field(name="All time", inline=True, value=
            "Volume: " + str(round(statsLuchadores['stats']['total_volume'] + statsPinatas['stats']['total_volume'] + statsWearables['stats']['total_volume'], 2)) + str(config["money_visual"]) + '\r' +
            "Sales: " + str(round(statsLuchadores['stats']['total_sales'] + statsPinatas['stats']['total_sales'] + statsWearables['stats']['total_sales'])) + '\r')
        embed.add_field(name='\u200B', inline=False, value='\u200B')
        embed.set_footer(text="luchadores.io", icon_url=config["lucha_icon_url"])
        return embed

luchaFloors.run(config["lucha_floor_token_id"])
