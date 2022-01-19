# -*- coding: utf-8 -*-
import discord
from discord.ext import commands 
from discord_slash import SlashCommand,SlashContext
from discord_slash.utils.manage_commands import create_choice,create_option
import nest_asyncio
import asyncio
intents=discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True


bot = commands.Bot(command_prefix='!',intents = intents)
slash = SlashCommand(bot, sync_commands=True)
 
@bot.event
async def on_ready():
    global ch , guilds
    print(">>Bot is online <<")
    
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(912947238957903872)
    await channel.send(f'歡迎新ㄉㄐㄐ {member} 加入!')
    print(f'{member} Join!')
    
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(912947238957903872)
    await channel.send(f'臭ㄐㄐ {member} 離開了!')
    print(f'{member} leave!')
    
@bot.event
async def on_raw_message_edit(payload):
    global userName,content
    
    channel = bot.get_channel(912947238957903872)
    channel_Name = bot.get_channel(payload.channel_id)
    try:
        if payload.data['content'].find('<@!') != -1 :
            while True:
                if payload.data['content'].find('<@!') == -1 :
                    break
                GetUserID = payload.data['content'][payload.data['content'].find('<@!')+3:payload.data['content'].find('<@!')+21]
                print(GetUserID)
                userName = await bot.fetch_user(GetUserID)
                await asyncio.sleep(1)
                print(userName)
                content = str(payload.data['content'])
                payload.data['content'] = content.replace(content[content.find('<@!'):content.find('<@!')+22], str(userName))
        elif payload.data['content'].find('<@') != -1 :
            while True:
                if payload.data['content'].find('<@') == -1 :
                    break
                GetUserID = payload.data['content'][payload.data['content'].find('<@')+2:payload.data['content'].find('<@')+20]
                print(GetUserID)
                userName = await bot.fetch_user(GetUserID)
                await asyncio.sleep(1)
                print(userName)
                content = str(payload.data['content'])
                payload.data['content'] = content.replace(content[content.find('<@'):content.find('<@')+21], str(userName))
        sendMessage = payload.data['author']['username']+"#"+payload.data['author']['discriminator'] +', '+channel_Name.name +', ' + payload.data['content']
        sendMessage2 = "https://discord.com/channels/" + payload.data["guild_id"] +"/" + payload.data["channel_id"]+"/"+str(payload.message_id)
        await channel.send(sendMessage)
        await channel.send(sendMessage2)
    except:
        sss =""
@bot.event
async def on_message(message):
    global a
    if message.channel.id == 898497922226860033:
        return
    if message.channel.id == 912947238957903872:
        return
    channel = bot.get_channel(912947238957903872)
    
    try:
        a = message
        check = True
        if len(message.content) != 0:
            if message.content.find('<@!') != -1 :
                while True:
                    if message.content.find('<@!') == -1 :
                        break
                    GetUserID = message.content[message.content.find('<@!')+3:message.content.find('<@!')+21]
                    print(GetUserID)
                    userName = await bot.fetch_user(GetUserID)
                    await asyncio.sleep(1)
                    print(userName)
                    content = str(message.content)
                    message.content = content.replace(content[content.find('<@!'):content.find('<@!')+22], str(userName))
            elif message.content.find('<@') != -1 :
                while True:
                    if message.content.find('<@') == -1 :
                        break
                    GetUserID = message.content[message.content.find('<@')+2:message.content.find('<@')+20]
                    print(GetUserID)
                    userName = await bot.fetch_user(GetUserID)
                    await asyncio.sleep(1)
                    print(userName)
                    content = str(message.content)
                    message.content = content.replace(content[content.find('<@'):content.find('<@')+21], str(userName))  
            sendMessage = message.author.name+"#"+message.author.discriminator+ ", "+ message.channel.name+", " + message.content
            await channel.send(sendMessage)
        if str(message.attachments[0]).find("https://") != -1:
            print(str(message.attachments[0]))
            sendMessage = message.author.name+"#"+message.author.discriminator+ ", "+ message.channel.name+", " + str(a.attachments[0])
            await channel.send(sendMessage)
    except:
        sss =""

def botRun():
    nest_asyncio.apply()
    bot.run("OTEzMjM3NzI1MTk1NDE5NjU4.YZ7k6A.8F95gaOh0Rge1osCXvMhJHqLlsw")


botRun()


    