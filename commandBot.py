# -*- coding: utf-8 -*-
import discord
from discord.ext import commands 
from discord_slash import SlashCommand,ComponentContext,MenuContext

from discord_slash.utils.manage_commands import create_choice,create_option
from discord_slash.utils.manage_components import *
from discord_slash.model import ButtonStyle,ContextMenuType

from discord_buttons_plugin import *

import nest_asyncio
import asyncio

from CommandClass import defaultCommand,DoroCommand
import json
from aiohttp import ClientSession

WEBHOOK_URL = 'https://discord.com/api/webhooks/915140137900462102/E34HrTfxgt7cKpfe0xI5V8uOZIlmSaRexjlc42PR9tZTbP9ikphQ2xHjX9NIKJKkYGB1'

webhook = ''
s = ''
if __name__ == '__main__':
    
    
    intents=discord.Intents.default()
    intents.members = True
    intents.reactions = True
    intents.messages = True
    
    
    
    bot = commands.Bot(command_prefix='!',intents = intents)
    slash = SlashCommand(bot, sync_commands=True)
    
    buttons = ButtonsClient(bot)
    jcard = []
    mylist = {}
    DoroSiteList =[]
    
    with open('setting.json','r',encoding="utf8") as jfile:
        jdata = json.load(jfile)
    for num in range (1,16):
        with open('Vol'+str(num)+'.json','r') as jfile:
            jcard.append(json.load(jfile))
    
    guild_ids = [jdata["guild"]]
    
    
    
    
    defaultCommand(bot,buttons,slash,guild_ids,jdata)
    
    DoroCommand(bot,buttons,slash, guild_ids, jcard,mylist,DoroSiteList)
    
    @bot.event
    async def on_select_option(interaction):
        if interaction.message.id == 891587821368905728: #Message id(not obligatory)
            await interaction.respond(type=6)
            if interaction.values[0] == "value1":
                await interaction.author.send("Menu 1")
            elif interaction.values[0] == "value2":
                await interaction.author.send("Menu 2")
    

    
    @slash.slash(name="Join_doro_1",
                     description="加入戰鬥城市_1",
                     guild_ids =guild_ids)
    async def _Join_doro_1(ctx):
        
        global s
        s= ctx
        channel = bot.get_channel(915166157512798250)
        await channel.set_permissions(ctx.author, read_messages=False,
                                                      send_messages=False)
        channel = bot.get_channel(915165983570788422)
        await channel.set_permissions(ctx.author, read_messages=True,
                                                      send_messages=True)   
        await ctx.send('發送一個測試')
    
    
    @slash.context_menu(target=ContextMenuType.MESSAGE,name="test2",
                        
                     guild_ids =guild_ids)
    async def _test(ctx:MenuContext):
        await ctx.send(
        content=f"Responded! The content of the message targeted: {ctx.target_message.content}",
        hidden=True
    )
    @slash.slash(name="whatthefuck",
                     description="發送一個測試",
                     guild_ids =guild_ids)
    async def _whatthefuck(ctx:ComponentContext):
        await ctx.send("My Message",hidden=True)
    
    @slash.slash(name="test",
                     description="發送一個測試",
                     guild_ids =guild_ids)
    async def _test(ctx:ComponentContext):
        global s
        s= ctx
        buttons = [
            create_button(
                style=ButtonStyle.green,
                label="A Green Button",
                custom_id='hello'
            ),
            create_button(
                style=ButtonStyle.green,
                label="A Green Button2",
                custom_id='hello22'
            )
          ]
        action_row = create_actionrow(*buttons)
        
        options=[# the options in your dropdown
                        create_select_option("Lab Coat", value="coat", emoji="🥼"),
                        create_select_option("Test Tube", value="tube", emoji="🧪"),
                        create_select_option("Petri Dish", value="dish", emoji="🧫"),
                        ]
        options.append(create_select_option("Lab Co2at", value="co2at", emoji="🥼"))
        
        select = create_select(options
                    ,custom_id='he1',
                    placeholder="Choose your option",  # the placeholder text to show when no options have been chosen
                    min_values=1,  # the minimum number of options a user must select
                    max_values=1  # the maximum number of options a user can select
                            )
        
        await ctx.send("test", components=[create_actionrow(select)])  # like action row with buttons but without * in front of the variable
        #await ctx.reply('123')
        #channel = bot.get_channel(ctx.channel_id)
        await ctx.send("My Message", components=[action_row],hidden=True)
        #await buttons.send('指令!!!',components=[ActionRow([Button(label="測試",style=ButtonType().Primary,custom_id="test_one")])],channel=ctx.channel_id)
    
    @slash.component_callback()
    async def hello(ctx: ComponentContext):
        global s
        s= ctx
        #<@!239007724744998912>
        await ctx.send(content=" 你ㄐㄐ很臭",hidden=True)
        
    @slash.component_callback()
    async def he1(ctx: ComponentContext):
        global s
        s= ctx
        await ctx.send(content=f"You selected {ctx.selected_options}")

    
    nest_asyncio.apply()
    bot.run(jdata["token"])
    