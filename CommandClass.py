# -*- coding: utf-8 -*-#
from discord_slash import SlashContext
from discord_slash.utils.manage_commands import create_choice,create_option,remove_slash_command
from upload import upload
from StatusClass import statusCreate
import random
import asyncio
class defaultCommand():
    def __init__(self,bot,slash, guild_ids,jdata):
        
        self.slash = slash
        self.guild_ids = guild_ids
        self.bot = bot
        self.jdata =jdata
        
        @self.bot.event
        async def on_ready():
            global here
            here = bot.get_guild(self.jdata["guild"])
            print(">>Bot is online <<")
            
        @self.slash.slash(name="moyen_Party",
                     description="魔眼派對",
                     guild_ids =self.guild_ids)
        async def _moyen_Party(ctx):
            await ctx.send(content="https://memeprod.ap-south-1.linodeobjects.com/user-gif/f617320247c594d021a00064f359fae5.gif")
        
        @self.slash.slash(name="sexual",
                     description="高潮",
                     guild_ids =self.guild_ids)
        async def _sexual(ctx):
            await ctx.send(content="https://tenor.com/view/%E9%87%8E%E7%8D%B8%E5%85%88%E8%BC%A9-gif-21736344")






mylist = []
Card_Choices = []
choices =[create_choice(name="狐狸",
                        value="你不要命了?挑戰 <@!1> 那你可是需要堤防他ㄉㄅㄐ!!!"
                        ),
          create_choice(name="丁py",
                        value="你竟然想挑戰 <@!1> piyen快洗乾淨ㄅ~~!!"
                        ),
          create_choice(name="醬汁",
                        value="<@!1> 只會私藏不教 無須挑戰"
                        ),
          create_choice(name="咩噗ㄐㄐ",
                        value="你竟敢挑戰 <@!1> !!!他可是至高咩噗"
                        )]


class DoroCommand():
    def __init__(self,slash, guild_ids,jcard):
        
        self.slash = slash
        self.guild_ids = guild_ids
        self.jcard = jcard
        

        @self.slash.slash(name="duel",
                     description="決鬥開始",
                     guild_ids =guild_ids)
        async def _duel(ctx):
            global sss 
            sss = ctx
            check = False
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author.name+"#"+ctx.author.discriminator:
                        check= True
                        break
            if check == False:
                mylist.append(statusCreate(ctx.author.name+"#"+ctx.author.discriminator,name=ctx.author.nick+"#"+ctx.author.discriminator))
                Card_Choices.append(create_choice(name=ctx.author.nick+"#"+ctx.author.discriminator,
                                value= ctx.author.name+"#"+ctx.author.discriminator
                                ))
                upload(Card_Choices)
            await ctx.send(content="決鬥開始!!!!")
        
        
        @self.slash.slash(name="Hp",
                     description="顯示剩餘血量",
                     guild_ids =guild_ids)
        async def _hp(ctx):
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author.name+"#"+ctx.author.discriminator:
                        await ctx.send("您的血量 : " + str(mylist[i].health))
                        return
            await ctx.send("找不到您的血量")
            
        @self.slash.slash(name="Number_of_cards",
                     description="顯示剩餘卡片",
                     guild_ids =guild_ids)
        async def _Number_of_cards(ctx):
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author.name+"#"+ctx.author.discriminator:
                        await ctx.send("您剩餘的卡片數量 : " + str(mylist[i].card))
                        return
            await ctx.send("找不到您的剩餘卡片")
            
        
        @self.slash.slash(name="pk",
                     description="打架",
                     guild_ids =guild_ids,
                     options=[
                         create_option(name="who",
                                       description="要跟誰PK?",
                                       option_type=3,
                                       required= True,
                                       choices=choices)])
        async def _pk(ctx:SlashContext,who:str):
            await ctx.send(who)
            
        @self.slash.slash(name="Attack",
                     description="攻擊",
                     guild_ids =guild_ids,
                     options=[create_option(name="who",
                               description="要攻擊誰?",
                               option_type=3,
                               required= True,
                               choices=Card_Choices)]
                         )
        async def _Attack(ctx:SlashContext,who:str):
            global aaa
            aaa= ctx
            if ctx.author.name+"#"+ctx.author.discriminator == who:
                await ctx.send("不可以攻擊自己")
            else :
                for i in range(len(mylist)):
                    if mylist[i].id == who:
                        if mylist[i].health <0:
                            await ctx.send(str(mylist[i].name) + "  已經葛屁了")
                            break
                        dechealth = random.randint(100,500)
                        await asyncio.sleep(1)
                        await ctx.send(str(mylist[i].name) +"遭受 " +ctx.author.nick+"#"+ctx.author.discriminator + " "+ str(dechealth) + "點的攻擊")
                        mylist[i].health = mylist[i].health - dechealth
                        if mylist[i].health <0:
                            await ctx.send(str(mylist[i].name) + "  葛屁了")
                            break
                        await ctx.send("剩下"+str(mylist[i].health))
                        break
                        
        @self.slash.slash(name="doro",
                     description="抽卡",
                     guild_ids =guild_ids)
        async def _doro(ctx):
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author.name+"#"+ctx.author.discriminator:
                        if mylist[i].card >0:
                            mylist[i].card = mylist[i].card -1
                            await ctx.send(mylist[i].name + " 抽了一張卡")
                            cardnum = random.randint(0, len(self.jcard)-1)
                            await ctx.send(self.jcard[cardnum]['src'])
                            return
                        else:
                            await ctx.send("找不到您的剩餘卡片")
            await ctx.send("你未參賽")
