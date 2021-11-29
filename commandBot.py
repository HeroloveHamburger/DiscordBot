# -*- coding: utf-8 -*-

from discord.ext import commands 

from discord_slash import SlashCommand

from CommandClass import defaultCommand

from CommandClass import DoroCommand

import nest_asyncio

import discord

import json


if __name__ == '__main__':
    
    
    intents=discord.Intents.default()
    intents.members = True
    intents.reactions = True
    intents.messages = True
    
    
    bot = commands.Bot(command_prefix='!',intents = intents)
    slash = SlashCommand(bot, sync_commands=True)
     

    with open('setting.json','r',encoding="utf8") as jfile:
        jdata = json.load(jfile)
    with open('card.json','r',encoding="utf8") as jfile:
        jcard = json.load(jfile)
    
    guild_ids = [jdata["guild"]]

    
    defaultCommand(bot,slash,guild_ids,jdata)
    DoroCommand(slash, guild_ids, jcard)
    
    nest_asyncio.apply()
    bot.run(jdata["token"])
    
