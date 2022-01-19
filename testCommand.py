# -*- coding: utf-8 -*-#
from discord_slash import SlashContext
from discord_slash.utils.manage_commands import create_choice,create_option,remove_slash_command
from upload import upload
from StatusClass import Player_Status,Doro_Site
import random
import asyncio
import os
import json

 


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

        @self.slash.slash(name="help",
                     description="幫助",
                     guild_ids =self.guild_ids)
        async def _help(ctx):
            await ctx.send(content="不會自己查?help三小?")







choices =[create_choice(name="狐狸",
                        value="你不要命了?挑戰 <@!303049625009389569> 那你可是需要堤防他ㄉㄅㄐ!!!"
                        ),
          create_choice(name="丁py",
                        value="你竟然想挑戰 <@!721728816086646885> piyen快洗乾淨ㄅ~~!!"
                        ),
          create_choice(name="醬汁",
                        value="<@!353540008176648192> 只會私藏不教 無須挑戰"
                        ),
          create_choice(name="咩噗ㄐㄐ",
                        value="你竟敢挑戰 <@!459010884547772416> !!!他可是至高咩噗"
                        )]
Card_Choices = []
Deck_Choices = []
arr = os.listdir('./套牌')

for i in range(len(arr)):
    Deckname = arr[i].replace('.json', "")
    Deck_Choices.append(create_choice(name=Deckname,
                        value=Deckname
                        ))

class DoroCommand():
    def __init__(self,bot,slash, guild_ids,jcard,mylist,DoroSiteList):
        self.bot = bot
        self.slash = slash
        self.guild_ids = guild_ids
        self.jcard = jcard
        
        @self.slash.slash(name="join_duel",
                     description="加入決鬥",
                     guild_ids =guild_ids)
        async def _join_duel(ctx):
            global sss 
            sss = ctx
            check = False
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author_id:
                        check= True
                        break
            if check == False:
                mylist.append(Player_Status(ctx.author_id,
                                           name=ctx.author.name+"#"+ctx.author.discriminator))
                Card_Choices.append(create_choice(name=ctx.author.name+"#"+ctx.author.discriminator,
                                value= str(ctx.author_id)
                                ))
                upload(Card_Choices)
            await ctx.send(content="加入決鬥!!!!")
        
        @self.slash.slash(name="leave",
                     description="退出決鬥",
                     guild_ids =guild_ids)
        async def _leave(ctx):
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author_id:
                        Card_Choices.pop(i)
                        upload(Card_Choices)
                        await ctx.send(mylist[i].name +" 離開決鬥")
                        mylist.pop(i)
                        channel = self.bot.get_channel(915166157512798250)
                        await channel.set_permissions(ctx.author, read_messages=False,
                                                                      send_messages=False)
                        channel = self.bot.get_channel(915165983570788422)
                        await channel.set_permissions(ctx.author, read_messages=False,
                                                                      send_messages=False)
                        return
            await ctx.send(content="你未開始決鬥，請先/duel")
        
        
        @self.slash.slash(name="Hp",
                     description="顯示剩餘血量",
                     guild_ids =guild_ids)
        async def _hp(ctx):
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author_id:
                        await ctx.send("您的血量 : " + str(mylist[i].health))
                        return
            await ctx.send("找不到您的血量")
            
        @self.slash.slash(name="Number_of_duels",
                     description="顯示當前決鬥者數量",
                     guild_ids =guild_ids)
        
        async def _Number_of_duels(ctx):
            await ctx.send("目前"+str(len(mylist)) +"位")
        
        @self.slash.slash(name="Number_of_cards",
                     description="顯示剩餘卡片",
                     guild_ids =guild_ids)
        async def _Number_of_cards(ctx):
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author_id:
                        await ctx.send("您剩餘的卡片數量 : " + str(mylist[i].cardNum))
                        return
            await ctx.send("找不到您的剩餘卡片")
        
        @self.slash.slash(name="Show_Deck",
                     description="顯示你目前的牌組",
                     guild_ids =guild_ids)
        async def _Show_Deck(ctx):
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author_id:
                        if len(mylist[i].DeckDict) !=0:
                            await ctx.send("你正在使用 : " + mylist[i].Deck + "牌組")
                            return
            await ctx.send("找不到您使用的牌組")
            
        @self.slash.slash(name="Show_AllCard",
                     description="顯示你目前的剩餘的卡片",
                     guild_ids =guild_ids)
        async def _Show_AllCard(ctx):
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author_id:
                        text=''
                        if len(mylist[i].DeckDict) !=0:
                            for k in mylist[i].cardDict.keys():
                                text = text + mylist[i].cardDict[k] +"\n"
                            await ctx.send(text)
                            return
            await ctx.send("找不到您使用的牌組")
        
        @self.slash.slash(name="Show_handCards",
                     description="顯示你手上的卡片",
                     guild_ids =guild_ids)
        async def _Show_handCards(ctx):
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author_id:
                        text=''
                        if len(mylist[i].handCards) !=0:
                            for k in range(0,len(mylist[i].handCards)):
                                for key in mylist[i].handCards[k].keys():
                                    text = text+mylist[i].handCards[k][str(key)]+"\n"
                            await ctx.send(text)
                            return
            await ctx.send("找不到您手上的卡片")
            
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
            
        
        @self.slash.slash(name="Challenge",
                     description="發起挑戰",
                     guild_ids =guild_ids,
                     options=[create_option(name="who",
                               description="對誰挑戰?",
                               option_type=3,
                               required= True,
                               choices=Card_Choices)]
                         )
        async def _challenge(ctx:SlashContext,who:str):
            global aaa
            aaa= ctx
            checkIsdoro = False
            own = -1
            if ctx.author_id == int(who):
                await ctx.send("不可以對自己挑戰")
            else :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author_id:
                        if len(mylist[i].DeckDict) ==0:
                            await ctx.send("<@!"+str(mylist[i].id)+"> 請先選擇套牌，在發起挑戰")
                            return
                        checkIsdoro = True
                        own = i
                        break
                    else:
                        checkIsdoro = False
                if checkIsdoro == False:
                    await ctx.send("你未參賽!!!請先/join_duel")
                    return
                for i in range(len(mylist)):
                    #對手
                    if mylist[i].id == int(who):
                        if len(mylist[i].DeckDict) ==0:
                            await ctx.send("對方尚未選擇套牌，無法挑戰")
                            return
                        #自己

                        if mylist[own].id == int(ctx.author_id):
                            
                            await ctx.send("<@!"+str(mylist[i].id)+"> \n"+mylist[own].name+"對你發起挑戰\n要接受嗎?")
                            mylist[i].challengBool = True
                            mylist[i].challenge_Author = ctx.author
                            mylist[i].challenge_Name = mylist[own].name
                            mylist[i].challenge_id = mylist[own].id
                            
                            mylist[own].challengBool = True
                            mylist[own].challenge_Name = mylist[i].name
                            mylist[own].challenge_id = mylist[i].id
                            break

        @self.slash.slash(name="Accept",
                     description="接受決鬥",
                     guild_ids =guild_ids)
        async def _accept(ctx):
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author_id:
                        #await ctx.send(""+str(mylist[i].challenge_id)+"")
                        #await ctx.send(""+str(mylist[i].challenge_Name)+"")
                        for k in range(len(mylist)):
                            if mylist[k].id == int(mylist[i].challenge_id) :
                                
                                mylist[i].doroStart = True
                                mylist[k].doroStart = True
                                #戰鬥1
                                channel = bot.get_channel(915165983570788422)
                                await channel.set_permissions(ctx.author, read_messages=True,
                                                                              send_messages=True)
                                #戰鬥2
                                channel = bot.get_channel(915166157512798250)
                                await channel.set_permissions(mylist[i].challenge_Author, read_messages=True,
                                                                              send_messages=True)
                                mylist[i].doro_Site = len(DoroSiteList)
                                mylist[k].doro_Site = len(DoroSiteList)
                                
                                DoroSiteList.append(Doro_Site(mylist[i],mylist[k]))
                                
                                await ctx.send("<@!"+str(mylist[k].id)+"> \n"+mylist[i].name+"以接受你的挑戰!\n"+
                                               "請<@!"+str(mylist[k].challenge_id)+">去戰鬥_1\n"+
                                               "請<@!"+str(mylist[k].id)+">去戰鬥_2")
                                if DoroSiteList[mylist[i].doro_Site].turn == 0:
                                    await ctx.send("由<@!"+str(mylist[i].id)+"> 先攻")
                                else:
                                    await ctx.send("由<@!"+str(mylist[k].id)+"> 先攻")
                                return
                            
            await ctx.send(content="你未開始決鬥，請先/join_duel")



        
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
            checkIsdoro = False
            if ctx.author_id == int(who):
                await ctx.send("不可以攻擊自己")
            else :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author_id:
                        checkIsdoro = True
                        break
                    else:
                        checkIsdoro = False
                if checkIsdoro == False:
                    await ctx.send("你未參賽!!!請先/join_duel")
                    return
                for i in range(len(mylist)):
                    if mylist[i].id == int(who):
                        if mylist[i].health <0:
                            await ctx.send(str(mylist[i].name) + "  已經葛屁了")
                            break
                        dechealth = random.randint(100,500)
                        await asyncio.sleep(1)
                        await ctx.send(str(mylist[i].name) +"遭受 " +ctx.author.name+"#"+ctx.author.discriminator + " "+ str(dechealth) + "點的攻擊")
                        mylist[i].health = mylist[i].health - dechealth
                        if mylist[i].health <0:
                            await ctx.send(str(mylist[i].name) + "  葛屁了")
                            break
                        await ctx.send("剩下"+str(mylist[i].health))
                        break
                        
                    
        @self.slash.slash(name="Select_Deck",
                     description="選擇牌組",
                     guild_ids =guild_ids,
                     options=[create_option(name="deck",
                               description="要選擇哪種套牌?",
                               option_type=3,
                               required= True,
                               choices=Deck_Choices)]
                         )
        async def _Select_Deck(ctx:SlashContext,deck:str):
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author_id:
                        mylist[i].Deck = deck
                        with open('./套牌/'+deck+'.json','r',encoding="utf8") as jfile:
                                DeckDictdata = json.load(jfile)
                        mylist[i].DeckDict = DeckDictdata
                        mylist[i].cardDict = DeckDictdata['名稱']
                        mylist[i].cardNum = len(DeckDictdata['名稱'])
                        await ctx.send(mylist[i].name +" 選擇了 "+deck +"牌組")
                        return
            await ctx.send(content="你未開始決鬥，請先/duel")            
        
        @self.slash.slash(name="duel",
                     description="決鬥開始",
                     guild_ids =guild_ids)
        async def _duel(ctx):
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author_id:
                        if len(mylist[i].DeckDict) ==0:
                            await ctx.send("找不到您使用的牌組")
                            return
                        if mylist[i].cardNum >0:
                            mylist[i].l = random.sample(range(0,len(mylist[i].cardDict)-1), len(mylist[i].cardDict)-1)
                            for k in range(0,5):
                                #print(k)
                                mylist[i].cardNum = mylist[i].cardNum -1
                                mylist[i].doroNum = mylist[i].doroNum +1
                                mylist[i].handCards.append({str(mylist[i].l[k]):str(mylist[i].cardDict[str(mylist[i].l[k])])})

                            await ctx.send("決鬥開始!!!\n抽五張牌")
                            return
                        else:
                            await ctx.send("你沒卡了")
            await ctx.send("你未參賽，請先/join_duel")
        
        @self.slash.slash(name="doro",
                     description="抽卡",
                     guild_ids =guild_ids)
        async def _doro(ctx):
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == ctx.author_id:
                        if len(mylist[i].DeckDict) ==0:
                            await ctx.send("找不到您使用的牌組")
                            return
                        if mylist[i].cardNum >0:
                            mylist[i].cardNum = mylist[i].cardNum -1
                            await ctx.send(mylist[i].name + " 抽了一張卡")
                            
                            one = random.randint(0, len(mylist[i].cardDict)-1)
                            
                            content = str("名稱 :"+mylist[i].DeckDict['名稱'][str(one)] +
                                           "\n"+
                                           "種類 :"+mylist[i].DeckDict['種類'][str(one)] +
                                           "\n"+
                                           "屬性 :"+mylist[i].DeckDict['屬性'][str(one)] +
                                           "\n"+
                                           "等級 :"+mylist[i].DeckDict['等級'][str(one)] +
                                           "\n"+
                                           "種族 :"+mylist[i].DeckDict['種族'][str(one)] +
                                           "\n"+
                                           "攻擊 :"+mylist[i].DeckDict['攻擊'][str(one)] +
                                           "\n"+
                                           "守備 :"+mylist[i].DeckDict['守備'][str(one)] +
                                           "\n"+
                                           "效果 :"+mylist[i].DeckDict['效果'][str(one)] )
                            
                            
                            if mylist[i].DeckDict['image_url'][str(one)] != '':
                                content = content + "\n" + mylist[i].DeckDict['image_url'][str(one)]
                            else:
                                content = content + "\n" + '沒有圖片'
                            
                            mylist[i].cardDict.pop(str(one))
                            await ctx.send(content)
                            return
                        else:
                            await ctx.send("你沒卡了")
            await ctx.send("你未參賽，請先/join_duel")
        
                    
        @self.slash.slash(name="ramdon_doro",
                     description="隨機抽卡",
                     guild_ids =guild_ids)
        async def _ramdon_doro(ctx):
            
                await ctx.send(ctx.author.name + " 抽了一張卡")
                one = random.randint(0, len(jcard)-1)
                two = random.randint(0, len(jcard[one]['image_url'])-1)
                
                content = str("名稱 :"+self.jcard[one]['名稱'][str(two)] +
                               "\n"+
                               "種類 :"+self.jcard[one]['種類'][str(two)] +
                               "\n"+
                               "屬性 :"+self.jcard[one]['屬性'][str(two)] +
                               "\n"+
                               "等級 :"+self.jcard[one]['等級'][str(two)] +
                               "\n"+
                               "種族 :"+self.jcard[one]['種族'][str(two)] +
                               "\n"+
                               "攻擊 :"+self.jcard[one]['攻擊'][str(two)] +
                               "\n"+
                               "守備 :"+self.jcard[one]['守備'][str(two)] +
                               "\n"+
                               "效果 :"+self.jcard[one]['效果'][str(two)] )
                
                
                if self.jcard[one]['image_url'][str(two)] != '':
                    content = content + "\n" + self.jcard[one]['image_url'][str(two)]
                else:
                    content = content + "\n" + '沒有圖片'
                    
                await ctx.send(content)
                            
                        