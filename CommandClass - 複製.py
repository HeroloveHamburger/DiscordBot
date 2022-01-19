# -*- coding: utf-8 -*-#
from discord_slash import SlashCommand,ComponentContext,SlashContext

from discord_slash.utils.manage_commands import create_choice,create_option
from discord_slash.utils.manage_components import *
from discord_slash.model import ButtonStyle
from upload import upload
from StatusClass import Player_Status,Doro_Site
import random
import asyncio
import os
import json

 


class defaultCommand():
    def __init__(self,bot,buttons,slash, guild_ids,jdata):
        
        self.slash = slash
        self.guild_ids = guild_ids
        self.bot = bot
        self.jdata =jdata
        self.buttons = buttons
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




Card_Choices = []
Deck_Choices = []
arr = os.listdir('./套牌')

buttons = [
            create_button(
                                label="加入決鬥!!!",
                                style=ButtonStyle.primary,
                                custom_id="join_duel"),
                             create_button(
                                label="顯示當前決鬥者數量",
                                style=ButtonStyle.primary,
                                custom_id="Number_of_duels"),
                            create_button(
                                label="離開決鬥",
                                style=ButtonStyle.primary,
                                custom_id="leave")
          ]
components = create_actionrow(*buttons)


for i in range(len(arr)):
    Deckname = arr[i].replace('.json', "")
    Deck_Choices.append(create_choice(name=Deckname,
                        value=Deckname
                        ))

class DoroCommand():
    def __init__(self,bot,buttons,slash, guild_ids,jcard,mylist,DoroSiteList):
        self.bot = bot
        self.slash = slash
        self.guild_ids = guild_ids
        self.jcard = jcard
        self.buttons = buttons

        @self.slash.slash(name="menu",
                     description="呼叫按鈕",
                     guild_ids =guild_ids)
        async def _menu(ctx:ComponentContext):
            await ctx.reply("指令!!!", components=[components])
        
        @slash.component_callback()
        #加入決鬥
        async def join_duel(ctx:ComponentContext):
            check = False
            mid = ctx.author_id
            mname = ctx.author.name+"#"+ctx.author.discriminator
            if len(mylist) !=0 :
                for i in range(len(mylist)):
                    if mylist[i].id == mid:
                        check= True
                        break
            if check == False:
                mylist.append(Player_Status(mid,
                                           name=mname))
                Card_Choices.append(create_choice(name=mname,
                                value= str(mid)
                                ))
                upload(Card_Choices)
                button = [
                            create_button(
                                label="選擇牌組",
                                style=ButtonStyle.primary,
                                custom_id="Select_Deck"),
                             create_button(
                                label="發起挑戰",
                                style=ButtonStyle.primary,
                                custom_id="Challenge")
                            ]
                
                components = create_actionrow(*button)
                await ctx.send(content= mname+"加入決鬥!!!!")
                await ctx.send(content= '可選擇的事情',components=[components],hidden=True)
                

            else:
                await ctx.edit_origin(content= mname+"已經加入過",hidden=True)
          
        @bot.event
        async def on_component(ctx:ComponentContext):
            custom_id = ctx.custom_id
            myid = ctx.author_id
            own = -1
            button = []
            if custom_id == 'Number_of_duels':
                await ctx.send("目前"+str(len(mylist)) +"位")
                return                
            if len(mylist) !=0 :
                    for i in range(len(mylist)):
                        if mylist[i].id == myid:
                            #選擇可用排組
                            if custom_id.find('Select_Deck_doro') !=-1:
                                deck = custom_id.replace('Select_Deck_doro','')
                                mylist[i].Deck = deck
                                print('./套牌/'+deck+'.json')
                                with open('./套牌/'+deck+'.json','r',encoding="utf8") as jfile:
                                        DeckDictdata = json.load(jfile)
                                mylist[i].DeckDict = DeckDictdata
                                #卡片順序
                                mylist[i].cardDict = random.sample(range(0,len(DeckDictdata['名稱'])-1), len(DeckDictdata['名稱'])-1)
                                mylist[i].cardNum = len(DeckDictdata['名稱'])
                                button = [
                                            create_button(
                                                label="選擇牌組",
                                                style=ButtonStyle.primary,
                                                custom_id="Select_Deck"),
                                             create_button(
                                                label="發起挑戰",
                                                style=ButtonStyle.primary,
                                                custom_id="Challenge")
                                            ]
                                
                                components = create_actionrow(*button)
                                await ctx.edit_origin(content=" 選擇了 "+deck +"牌組",components=[components]) 
                                return
                            
                            #點選選擇排組按鈕
                            elif custom_id =='Select_Deck' :
                                for k in range(len(arr)):
                                    Deckname = arr[k].replace('.json', "")
                                    button.append(create_button(
                                        label=Deckname,
                                        style=ButtonStyle.primary,
                                        custom_id='Select_Deck_doro'+Deckname))
                                components = create_actionrow(*button)
                                await ctx.edit_origin(content="可選擇的套排",components=[components]) 
                                return
                            elif custom_id =='Challenge' :
                                for k in range(len(mylist)):
                                    if mylist[k].id==myid :
                                        continue
                                    button.append(create_button(
                                    label=mylist[k].name,
                                    style=ButtonStyle.primary,
                                    custom_id="Challenge_to"+str(mylist[k].id)))
                                    components = create_actionrow(*button)
                                if len(button) !=0:
                                    await ctx.edit_origin(content="可選擇的挑戰對象",components=[components],hidden=True) 
                                else:
                                    await ctx.edit_origin(content="無人可挑戰",hidden=True) 
                                return
                            
                            elif custom_id.find('Challenge_to') !=-1 :
                                who = custom_id.replace('Challenge_to','')
                                if ctx.author_id == int(who):
                                    await ctx.edit_origin(content="不可以對自己挑戰")
                                    return

                                if len(mylist[i].DeckDict) ==0:
                                    await ctx.edit_origin(content="<@!"+str(mylist[i].id)+"> 請先選擇套牌，在發起挑戰")
                                    return
                                        
                                for k in range(len(mylist)):
                                    #對手
                                    if mylist[k].id == int(who):
                                        if len(mylist[k].DeckDict) ==0:
                                            await ctx.edit_origin(content="對方尚未選擇套牌，無法挑戰")
                                            return
                                        #自己

                                        if mylist[i].id == int(ctx.author_id):
                                            
                                            buttons = [
                                                        create_button(
                                                                       label="接受!!!",
                                                                       style=ButtonStyle.primary,
                                                                       custom_id="Accept"+str(mylist[k].id)),
                                                                    create_button(
                                                                       label="拒絕!!!",
                                                                       style=ButtonStyle.primary,
                                                                       custom_id="UnAccept"),
                                                                        
                                                      ]
                                            components = create_actionrow(*buttons)
                                            await ctx.send("<@!"+str(mylist[k].id)+"> \n"+mylist[i].name+"對你發起挑戰\n要接受嗎?",components=[components])
                                            mylist[k].challengBool = True
                                            mylist[k].challenge_Author = ctx.author
                                            mylist[k].challenge_Name = mylist[i].name
                                            mylist[k].challenge_id = mylist[i].id
                                            
                                            mylist[i].challengBool = True
                                            mylist[i].challenge_Name = mylist[k].name
                                            mylist[i].challenge_id = mylist[k].id
                                            return
                                        
                            elif custom_id.find('Accept') !=-1 :
                                who = custom_id.replace('Accept','')
                                print(who)
                                print(ctx.author_id)
                                if ctx.author_id != int(who):
                                    await ctx.send("你無法使用此按鈕",hidden=True)
                                    return
                                for k in range(len(mylist)):
                                    if mylist[k].id == int(mylist[i].challenge_id) :
                                        
                                        mylist[i].doroStart = True
                                        mylist[k].doroStart = True
                                        
                                        mylist[i].doro_Site = len(DoroSiteList)
                                        mylist[k].doro_Site = len(DoroSiteList)
                                        
                                        DoroSiteList.append(Doro_Site(mylist[i],mylist[k]))
                                        
                                        buttons = [
                                            create_button(
                                                           label="決鬥開始!!!",
                                                           style=ButtonStyle.primary,
                                                           custom_id="duel")
                                          ]
                                        components = create_actionrow(*buttons)
                                        
                                        await ctx.send("<@!"+str(mylist[k].id)+"> \n"+mylist[i].name+"以接受你的挑戰!\n",components =[components])
                                        if DoroSiteList[mylist[i].doro_Site].turn == 0:
                                            await ctx.send("由<@!"+str(mylist[i].id)+"> 先攻")
                                        else:
                                            await ctx.send("由<@!"+str(mylist[k].id)+"> 先攻")
    
                                        return
                                
                            elif custom_id =='action':
                                if mylist[i].doro_Site == -1:
                                    await ctx.send("你沒有在決鬥場",hidden=True)
                                    return
                                if DoroSiteList[mylist[i].doro_Site].P1_Status.id == ctx.author_id:
                                    await is_action(ctx,DoroSiteList[mylist[i].doro_Site].P1_Status.health,DoroSiteList[mylist[i].doro_Site].P1_Status.is_doro)
                                elif DoroSiteList[mylist[i].doro_Site].P2_Status.id == ctx.author_id:
                                    await is_action(ctx,DoroSiteList[mylist[i].doro_Site].P2_Status.health,DoroSiteList[mylist[i].doro_Site].P2_Status.is_doro)
                                return
                            
                            elif custom_id == 'duel':
                                if mylist[i].doro_Site == -1:
                                    await ctx.send("你沒有在決鬥場",hidden=True)
                                    return
                                if DoroSiteList[mylist[i].doro_Site].P1_Status.id == ctx.author_id:
                                    if DoroSiteList[mylist[i].doro_Site].P1_Status.first_doro == True:
                                        await ctx.edit_origin(content="你不能再抽五張卡")
                                        return
                                    
                                    for kk in range(0,5):
                                        #print(k)
                                        DoroSiteList[mylist[i].doro_Site].P1_Status.cardNum = DoroSiteList[mylist[i].doro_Site].P1_Status.cardNum -1
                                        DoroSiteList[mylist[i].doro_Site].P1_Status.handCards.append(DoroSiteList[mylist[i].doro_Site].P1_Status.cardDict[0])
                                        DoroSiteList[mylist[i].doro_Site].P1_Status.cardDict.pop(0)
                                    await ctx.send("<@!"+str(mylist[i].id)+">決鬥開始!!!\n抽五張牌")
                                    DoroSiteList[mylist[i].doro_Site].P1_Status.first_doro = True
                                    
                                    await dorofun(ctx,DoroSiteList[mylist[i].doro_Site].P1_Status.health)
                                    return
                                elif DoroSiteList[mylist[i].doro_Site].P2_Status.id == ctx.author_id:
                                    if DoroSiteList[mylist[i].doro_Site].P2_Status.first_doro == True:
                                        await ctx.edit_origin(content="你不能再抽五張卡",hidden=True)
                                        return
                                    for kk in range(0,5):
                                        DoroSiteList[mylist[i].doro_Site].P2_Status.cardNum = DoroSiteList[mylist[i].doro_Site].P2_Status.cardNum -1
                                        DoroSiteList[mylist[i].doro_Site].P2_Status.handCards.append(DoroSiteList[mylist[i].doro_Site].P2_Status.cardDict[0])
                                        DoroSiteList[mylist[i].doro_Site].P2_Status.cardDict.pop(0)
                                    await ctx.send("<@!"+str(mylist[i].id)+">決鬥開始!!!\n抽五張牌")
                                    DoroSiteList[mylist[i].doro_Site].P2_Status.first_doro = True
                                    
                                    await dorofun(ctx,DoroSiteList[mylist[i].doro_Site].P2_Status.health)
                                    return
                                
                            elif custom_id == 'doro':
                                
                                if len(mylist[i].DeckDict) ==0:
                                    await ctx.edit_origin(content="找不到您使用的牌組")
                                    return
                                
                                if DoroSiteList[mylist[i].doro_Site].P1_Status.id == ctx.author_id:
                                    if DoroSiteList[mylist[i].doro_Site].turn == 1:
                                        await ctx.edit_origin(content="還不到你的回合，不能抽卡",hidden=True)
                                        return
                                    if DoroSiteList[mylist[i].doro_Site].P1_Status.is_doro == 0:
                                        await ctx.edit_origin(content="你已經抽過卡，請等下一回合",hidden=True)
                                        return
                                    
                                    if DoroSiteList[mylist[i].doro_Site].P1_Status.cardNum ==0:
                                        await ctx.edit_origin(content="你沒卡了",hidden=True)
                                        return
                                    DoroSiteList[mylist[i].doro_Site].P1_Status.is_doro = DoroSiteList[mylist[i].doro_Site].P1_Status.is_doro -1
                                    DoroSiteList[mylist[i].doro_Site].P1_Status.cardNum = DoroSiteList[mylist[i].doro_Site].P1_Status.cardNum -1
                                    DoroSiteList[mylist[i].doro_Site].P1_Status.handCards.append(DoroSiteList[mylist[i].doro_Site].P1_Status.cardDict[0])
                                    
                                    await ctx.edit_origin(content="執行指令",components=[],hidden=True)
                                    await ctx.send(DoroSiteList[mylist[i].doro_Site].P1_Status.name + " 抽了一張卡")
                                
                                    content = str("名稱 :"+mylist[i].DeckDict['名稱'][str(DoroSiteList[mylist[i].doro_Site].P1_Status.cardDict[0])] +
                                                   "\n"+
                                                   "種類 :"+mylist[i].DeckDict['種類'][str(DoroSiteList[mylist[i].doro_Site].P1_Status.cardDict[0])] +
                                                   "\n"+
                                                   "屬性 :"+mylist[i].DeckDict['屬性'][str(DoroSiteList[mylist[i].doro_Site].P1_Status.cardDict[0])] +
                                                   "\n"+
                                                   "等級 :"+mylist[i].DeckDict['等級'][str(DoroSiteList[mylist[i].doro_Site].P1_Status.cardDict[0])] +
                                                   "\n"+
                                                   "種族 :"+mylist[i].DeckDict['種族'][str(DoroSiteList[mylist[i].doro_Site].P1_Status.cardDict[0])] +
                                                   "\n"+
                                                   "攻擊 :"+mylist[i].DeckDict['攻擊'][str(DoroSiteList[mylist[i].doro_Site].P1_Status.cardDict[0])] +
                                                   "\n"+
                                                   "守備 :"+mylist[i].DeckDict['守備'][str(DoroSiteList[mylist[i].doro_Site].P1_Status.cardDict[0])] +
                                                   "\n"+
                                                   "效果 :"+mylist[i].DeckDict['效果'][str(DoroSiteList[mylist[i].doro_Site].P1_Status.cardDict[0])] )
                                    
                                    
                                    if mylist[i].DeckDict['image_url'][str(DoroSiteList[mylist[i].doro_Site].P1_Status.cardDict[0])] != '':
                                        content = content + "\n" + mylist[i].DeckDict['image_url'][str(DoroSiteList[mylist[i].doro_Site].P1_Status.cardDict[0])]
                                    else:
                                        content = content + "\n" + '沒有圖片'
                                    
                                    DoroSiteList[mylist[i].doro_Site].P1_Status.cardDict.pop(0)
                                    await ctx.send(content,hidden=True)
                                    await dorofun(ctx,DoroSiteList[mylist[i].doro_Site].P1_Status.health)
                                    return
                                
                                
                                
                                elif DoroSiteList[mylist[i].doro_Site].P2_Status.id == ctx.author_id:
                                    if DoroSiteList[mylist[i].doro_Site].turn == 0:
                                        await ctx.edit_origin(content="還不到你的回合，不能抽卡",hidden=True)
                                        return
                                    if DoroSiteList[mylist[i].doro_Site].P2_Status.is_doro == 0:
                                        await ctx.edit_origin(content="你已經抽過卡，請等下一回合",hidden=True)
                                        return
                                    if DoroSiteList[mylist[i].doro_Site].P2_Status.cardNum ==0:
                                        await ctx.edit_origin(content="你沒卡了",hidden=True)
                                        return
                                    DoroSiteList[mylist[i].doro_Site].P2_Status.is_doro = DoroSiteList[mylist[i].doro_Site].P2_Status.is_doro -1
                                    DoroSiteList[mylist[i].doro_Site].P2_Status.cardNum = DoroSiteList[mylist[i].doro_Site].P2_Status.cardNum -1
                                    DoroSiteList[mylist[i].doro_Site].P2_Status.handCards.append(DoroSiteList[mylist[i].doro_Site].P2_Status.cardDict[0])
                                    
                                    await ctx.edit_origin(content="執行指令",components=[],hidden=True)
                                    
                                    await ctx.send(DoroSiteList[mylist[i].doro_Site].P2_Status.name + " 抽了一張卡")
                                
                                    content = str("名稱 :"+mylist[i].DeckDict['名稱'][str(DoroSiteList[mylist[i].doro_Site].P2_Status.cardDict[0])] +
                                                   "\n"+
                                                   "種類 :"+mylist[i].DeckDict['種類'][str(DoroSiteList[mylist[i].doro_Site].P2_Status.cardDict[0])] +
                                                   "\n"+
                                                   "屬性 :"+mylist[i].DeckDict['屬性'][str(DoroSiteList[mylist[i].doro_Site].P2_Status.cardDict[0])] +
                                                   "\n"+
                                                   "等級 :"+mylist[i].DeckDict['等級'][str(DoroSiteList[mylist[i].doro_Site].P2_Status.cardDict[0])] +
                                                   "\n"+
                                                   "種族 :"+mylist[i].DeckDict['種族'][str(DoroSiteList[mylist[i].doro_Site].P2_Status.cardDict[0])] +
                                                   "\n"+
                                                   "攻擊 :"+mylist[i].DeckDict['攻擊'][str(DoroSiteList[mylist[i].doro_Site].P2_Status.cardDict[0])] +
                                                   "\n"+
                                                   "守備 :"+mylist[i].DeckDict['守備'][str(DoroSiteList[mylist[i].doro_Site].P2_Status.cardDict[0])] +
                                                   "\n"+
                                                   "效果 :"+mylist[i].DeckDict['效果'][str(DoroSiteList[mylist[i].doro_Site].P2_Status.cardDict[0])] )
                                    
                                    
                                    if mylist[i].DeckDict['image_url'][str(DoroSiteList[mylist[i].doro_Site].P2_Status.cardDict[0])] != '':
                                        content = content + "\n" + mylist[i].DeckDict['image_url'][str(DoroSiteList[mylist[i].doro_Site].P2_Status.cardDict[0])]
                                    else:
                                        content = content + "\n" + '沒有圖片'
                                    
                                    DoroSiteList[mylist[i].doro_Site].P2_Status.cardDict.pop(0)
                                    await ctx.send(content,hidden=True)
                                    await dorofun(ctx,DoroSiteList[mylist[i].doro_Site].P2_Status.health)
                                    return
                            elif custom_id == 'Show_handCards':
                                text=''
                                if mylist[i].doro_Site == -1:
                                    await ctx.send("你沒有在決鬥場",hidden=True)
                                    break
                                if DoroSiteList[mylist[i].doro_Site].P1_Status.id == ctx.author_id:
                                    
                                    if len(DoroSiteList[mylist[i].doro_Site].P1_Status.handCards) !=0:
                                        options=[]
                                        for k in range(0,len(DoroSiteList[mylist[i].doro_Site].P1_Status.handCards)):
                                            num = DoroSiteList[mylist[i].doro_Site].P1_Status.handCards[k]
                                            options.append(create_select_option(str(mylist[i].DeckDict["名稱"][str(num)]), value="show_selectCard_"+str(num), emoji="🥼"))
                                        select = create_select(options,
                                                               custom_id='show_handCard',
                                                               placeholder="這是你手上的卡",  # the placeholder text to show when no options have been chosen
                                                               min_values=1,  # the minimum number of options a user must select
                                                               max_values=1  # the maximum number of options a user can select
                                                                        )
                                        buttons = [         
                                            create_button(                                                         
                                                    label="返回",
                                                    style=ButtonStyle.primary,
                                                    custom_id="return_menu")
                                                    ]
                                        await ctx.edit_origin(content='你的手牌',components=[create_actionrow(select),create_actionrow(*buttons)],hidden=True)
                                        return
                                elif DoroSiteList[mylist[i].doro_Site].P2_Status.id == ctx.author_id:
                                    
                                    if len(DoroSiteList[mylist[i].doro_Site].P2_Status.handCards) !=0:
                                        options=[]
                                        for k in range(0,len(DoroSiteList[mylist[i].doro_Site].P2_Status.handCards)):
                                            num = DoroSiteList[mylist[i].doro_Site].P2_Status.handCards[k]
                                            options.append(create_select_option(str(mylist[i].DeckDict["名稱"][str(num)]), value="show_selectCard_"+str(num), emoji="🥼"))
                                        select = create_select(options,
                                                               custom_id='show_handCard',
                                                               placeholder="這是你手上的卡",  # the placeholder text to show when no options have been chosen
                                                               min_values=1,  # the minimum number of options a user must select
                                                               max_values=1  # the maximum number of options a user can select
                                                                        )
                                        
                                        buttons = [         
                                            create_button(                                                         
                                                    label="返回",
                                                    style=ButtonStyle.primary,
                                                    custom_id="return_menu")
                                                    ]
           
                                        await ctx.edit_origin(content='你的手牌',components=[create_actionrow(select),create_actionrow(*buttons)],hidden=True)
                                        return
                                    
                            elif custom_id =='Show_GraveCards':
                                text=''
                                if mylist[i].doro_Site == -1:
                                    await ctx.send("你沒有在決鬥場",hidden=True)
                                    break
                                if DoroSiteList[mylist[i].doro_Site].P1_Status.id == ctx.author_id:
                                    
                                        
                                    if len(DoroSiteList[mylist[i].doro_Site].P1_Status.cardDictGrave) !=0:
                                        for k in range(0,len(DoroSiteList[mylist[i].doro_Site].P1_Status.cardDictGrave)):
                                            num = DoroSiteList[mylist[i].doro_Site].P1_Status.handCards[k]
                                            options.append(create_select_option(str(mylist[i].DeckDict["名稱"][str(num)]), value="show_selectCard_"+str(num), emoji="🥼"))
                                        select = create_select(options,
                                                               custom_id='show_handCard',
                                                               placeholder="這是你手上的卡",  # the placeholder text to show when no options have been chosen
                                                               min_values=1,  # the minimum number of options a user must select
                                                               max_values=1  # the maximum number of options a user can select
                                                                        )
                                        buttons = [         
                                            create_button(                                                         
                                                    label="返回",
                                                    style=ButtonStyle.primary,
                                                    custom_id="return_menu")
                                                    ]
                                        await ctx.edit_origin(content='你的手牌',components=[create_actionrow(select),create_actionrow(*buttons)],hidden=True)
                                        return
                                    else:
                                        await ctx.edit_origin(content="你的墳墓沒有任何卡片",hidden=True)
                                        return
                                elif DoroSiteList[mylist[i].doro_Site].P2_Status.id == ctx.author_id:
                                    
                                    if len(DoroSiteList[mylist[i].doro_Site].P2_Status.cardDictGrave) !=0:
                                        for k in range(0,len(DoroSiteList[mylist[i].doro_Site].P2_Status.cardDictGrave)):
                                            num = DoroSiteList[mylist[i].doro_Site].P2_Status.handCards[k]
                                            options.append(create_select_option(str(mylist[i].DeckDict["名稱"][str(num)]), value="show_selectCard_"+str(num), emoji="🥼"))
                                        select = create_select(options,
                                                               custom_id='show_handCard',
                                                               placeholder="這是你手上的卡",  # the placeholder text to show when no options have been chosen
                                                               min_values=1,  # the minimum number of options a user must select
                                                               max_values=1  # the maximum number of options a user can select
                                                                        )
                                        
                                        buttons = [         
                                            create_button(                                                         
                                                    label="返回",
                                                    style=ButtonStyle.primary,
                                                    custom_id="return_menu")
                                                    ]
           
                                        await ctx.edit_origin(content='你的手牌',components=[create_actionrow(select),create_actionrow(*buttons)],hidden=True)
                                        return
                                    else:
                                        await ctx.edit_origin(content="你的墳墓沒有任何卡片",hidden=True)
                                        return
                            
                            elif custom_id == 'select_card':
                                    text=''
                                    if mylist[i].doro_Site == -1:
                                        await ctx.send("你沒有在決鬥場",hidden=True)
                                        break
                                    if DoroSiteList[mylist[i].doro_Site].P1_Status.id == ctx.author_id:
                                        
                                        if len(DoroSiteList[mylist[i].doro_Site].P1_Status.handCards) !=0:
                                            button = [  
                                                        create_button(
                                                                    label='怪獸卡',
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="monster_card"),
                                                        create_button(
                                                                    label='魔法卡',
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="magic_card"),
                                                        create_button(
                                                                    label='陷阱卡',
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="trap_card"),
                                                               
                                                        create_button(                                                         
                                                                    label="返回",
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="return_menu")
                                                                    
                                                    ]
                                            
                                            components = create_actionrow(*button)
                                            
                                            await ctx.edit_origin(content='手上的卡片',components=[components],hidden=True)
                                            return
                                    elif DoroSiteList[mylist[i].doro_Site].P2_Status.id == ctx.author_id:
                                        
                                        if len(DoroSiteList[mylist[i].doro_Site].P2_Status.handCards) !=0:
                                            button = [  
                                                       create_button(
                                                                   label='怪獸卡',
                                                                   style=ButtonStyle.primary,
                                                                   custom_id="monster_card"),
                                                       create_button(
                                                                   label='魔法卡',
                                                                   style=ButtonStyle.primary,
                                                                   custom_id="magic_card"),
                                                       create_button(
                                                                   label='陷阱卡',
                                                                   style=ButtonStyle.primary,
                                                                   custom_id="trap_card"),
                                                       create_button(                                                         
                                                                    label="返回",
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="return_menu")
                                                   ]
                                            components = create_actionrow(*button)
                                                
                                            await ctx.edit_origin(content='手上的卡片',components=[components],hidden=True)
                                            return
                                        
                            elif custom_id =='finish_turn':
                                    
                                if len(mylist[i].DeckDict) ==0:
                                    await ctx.send("找不到您使用的牌組")
                                    return
                                
                                if DoroSiteList[mylist[i].doro_Site].P1_Status.id == ctx.author_id:
                                    if DoroSiteList[mylist[i].doro_Site].turn == 1:
                                        await ctx.send("還不到你的回合，不能結束",hidden=True)
                                        await dorofun(ctx,DoroSiteList[mylist[i].doro_Site].P1_Status.health)
                                        return
                                    if DoroSiteList[mylist[i].doro_Site].P1_Status.is_doro >0:
                                        await ctx.send("卡片能抽數量未抽完，不能結束",hidden=True)
                                        await dorofun(ctx,DoroSiteList[mylist[i].doro_Site].P1_Status.health)
                                        return
                                    print('p1')
                                    DoroSiteList[mylist[i].doro_Site].P1_Status.is_doro = 1
                                    DoroSiteList[mylist[i].doro_Site].turn = DoroSiteList[mylist[i].doro_Site].turn +1
                                    await ctx.send("<@!"+str(mylist[i].id)+">回合結束!!!\n輪到<@!"+str(DoroSiteList[mylist[i].doro_Site].P2_Status.id)+">回合")
                                    
                                    
                                    await dorofun(ctx,DoroSiteList[mylist[i].doro_Site].P1_Status.health)
                                    return
                                    
                                    
                                    
                                elif DoroSiteList[mylist[i].doro_Site].P2_Status.id == ctx.author_id:
                                    if DoroSiteList[mylist[i].doro_Site].turn == 0:
                                        await ctx.send("還不到你的回合，不能結束",hidden=True)
                                        await dorofun(ctx,DoroSiteList[mylist[i].doro_Site].P2_Status.health)
                                        return
                                    if DoroSiteList[mylist[i].doro_Site].P2_Status.is_doro >0:
                                        await ctx.send("卡片能抽數量未抽完，不能結束",hidden=True)
                                        await dorofun(ctx,DoroSiteList[mylist[i].doro_Site].P2_Status.health)
                                        return
                                    print('p2')
                                    DoroSiteList[mylist[i].doro_Site].P2_Status.is_doro = 1
                                    DoroSiteList[mylist[i].doro_Site].turn = DoroSiteList[mylist[i].doro_Site].turn -1
                                    await ctx.send("<@!"+str(mylist[i].id)+">回合結束!!!\n輪到<@!"+str(DoroSiteList[mylist[i].doro_Site].P1_Status.id)+">回合")
                                    await dorofun(ctx,DoroSiteList[mylist[i].doro_Site].P2_Status.health)
                                    return
                                
                            elif custom_id =='monster_card':
                                
                                if DoroSiteList[mylist[i].doro_Site].P1_Status.id == ctx.author_id:
                            
                                    if len(DoroSiteList[mylist[i].doro_Site].P1_Status.handCards) !=0:
                                        options=[create_select_option('請選擇', value="select_monster_card_None", emoji="🥼")]
                                        for k in range(0,len(DoroSiteList[mylist[i].doro_Site].P1_Status.handCards)):
                                            num = DoroSiteList[mylist[i].doro_Site].P1_Status.handCards[k]
                                            if str(mylist[i].DeckDict["種類"][str(num)]).find("怪獸") == -1:
                                                   continue
                                            options.append(create_select_option(str(mylist[i].DeckDict["名稱"][str(num)]), value="select_monster_card_"+str(num), emoji="🥼"))
                                        if len(options) >1:
                                            select = create_select(options,
                                                                   custom_id='show_wand_selectCard',
                                                                   placeholder="這是你手上的卡",  # the placeholder text to show when no options have been chosen
                                                                   min_values=1,  # the minimum number of options a user must select
                                                                   max_values=1  # the maximum number of options a user can select
                                                                            )
                                            buttons = [         
                                            create_button(                                                         
                                                    label="返回",
                                                    style=ButtonStyle.primary,
                                                    custom_id="return_menu")
                                                    ]
                                            await ctx.edit_origin(content='你選擇的種類卡',components=[create_actionrow(select),create_actionrow(*buttons)],hidden=True)
                                            return
                                elif DoroSiteList[mylist[i].doro_Site].P2_Status.id == ctx.author_id:
                                    if len(DoroSiteList[mylist[i].doro_Site].P2_Status.handCards) !=0:
                                        options=[create_select_option('請選擇', value="select_monster_card_None", emoji="🥼")]
                                        for k in range(0,len(DoroSiteList[mylist[i].doro_Site].P2_Status.handCards)):
                                            num = DoroSiteList[mylist[i].doro_Site].P2_Status.handCards[k]
                                            if str(mylist[i].DeckDict["種類"][str(num)]).find("怪獸") == -1:
                                                   continue
                                            options.append(create_select_option(str(mylist[i].DeckDict["名稱"][str(num)]), value="select_monster_card_"+str(num), emoji="🥼"))
                                        if len(options) >1:
                                           select = create_select(options,
                                                                  custom_id='show_wand_selectCard',
                                                                  placeholder="你選擇的種類卡",  # the placeholder text to show when no options have been chosen
                                                                  min_values=1,  # the minimum number of options a user must select
                                                                  max_values=1  # the maximum number of options a user can select
                                                                           )
                                           buttons = [         
                                            create_button(                                                         
                                                    label="返回",
                                                    style=ButtonStyle.primary,
                                                    custom_id="return_menu")
                                                    ]
                                           await ctx.edit_origin(content='你選擇的種類卡',components=[create_actionrow(select),create_actionrow(*buttons)],hidden=True)
                                           return
                                    
                                await ctx.edit_origin(content='你手上沒有怪獸卡',hidden=True)
                                return
                                
                            elif custom_id =='magic_card':
                                
                                if mylist[i].doro_Site == -1:
                                    await ctx.send("你沒有在決鬥場",hidden=True)
                                    break
                                if DoroSiteList[mylist[i].doro_Site].P1_Status.id == ctx.author_id:
                                    options=[create_select_option('請選擇', value="select_magic_card_None", emoji="🥼")]
                                    if len(DoroSiteList[mylist[i].doro_Site].P1_Status.handCards) !=0:
                                        
                                        for k in range(0,len(DoroSiteList[mylist[i].doro_Site].P1_Status.handCards)):
                                            num = DoroSiteList[mylist[i].doro_Site].P1_Status.handCards[k]
                                            if str(mylist[i].DeckDict["種類"][str(num)]).find("魔法") == -1:
                                                   continue
                                            options.append(create_select_option(str(mylist[i].DeckDict["名稱"][str(num)]), value="select_magic_card_"+str(num), emoji="🥼"))
                                        if len(options) >1:
                                            select = create_select(options,
                                                                   custom_id='show_wand_selectCard',
                                                                   placeholder="這是你手上的卡",  # the placeholder text to show when no options have been chosen
                                                                   min_values=1,  # the minimum number of options a user must select
                                                                   max_values=1  # the maximum number of options a user can select
                                                                            )
                                            buttons = [         
                                            create_button(                                                         
                                                    label="返回",
                                                    style=ButtonStyle.primary,
                                                    custom_id="return_menu")
                                                    ]
                                            await ctx.edit_origin(content='你選擇的種類卡',components=[create_actionrow(select),create_actionrow(*buttons)],hidden=True)
                                            return
                                elif DoroSiteList[mylist[i].doro_Site].P2_Status.id == ctx.author_id:
                                    if len(DoroSiteList[mylist[i].doro_Site].P2_Status.handCards) !=0:
                                        options=[create_select_option('請選擇', value="select_magic_card_None", emoji="🥼")]
                                        for k in range(0,len(DoroSiteList[mylist[i].doro_Site].P2_Status.handCards)):
                                            num = DoroSiteList[mylist[i].doro_Site].P2_Status.handCards[k]
                                            if str(mylist[i].DeckDict["種類"][str(num)]).find("魔法") == -1:
                                                   continue
                                            options.append(create_select_option(str(mylist[i].DeckDict["名稱"][str(num)]), value="select_magic_card_"+str(num), emoji="🥼"))
                                        if len(options) >1:
                                            select = create_select(options,
                                                                   custom_id='show_wand_selectCard',
                                                                   placeholder="你選擇的種類卡",  # the placeholder text to show when no options have been chosen
                                                                   min_values=1,  # the minimum number of options a user must select
                                                                   max_values=1  # the maximum number of options a user can select
                                                                            )
                                            
                                            buttons = [         
                                            create_button(                                                         
                                                    label="返回",
                                                    style=ButtonStyle.primary,
                                                    custom_id="return_menu")
                                                    ]
                                            await ctx.edit_origin(content='你選擇的種類卡',components=[create_actionrow(select),create_actionrow(*buttons)],hidden=True)
                                            return
                                 
                                await ctx.edit_origin(content='你手上沒有魔法卡',hidden=True)
                                return
                            
                            
                            elif custom_id =='trap_card':
                                
                                if mylist[i].doro_Site == -1:
                                    await ctx.send("你沒有在決鬥場",hidden=True)
                                    break
                                if DoroSiteList[mylist[i].doro_Site].P1_Status.id == ctx.author_id:
                                    if len(DoroSiteList[mylist[i].doro_Site].P1_Status.handCards) !=0:
                                        options=[create_select_option('請選擇', value="select_trap_card_None", emoji="🥼")]
                                        for k in range(0,len(DoroSiteList[mylist[i].doro_Site].P1_Status.handCards)):
                                            num = DoroSiteList[mylist[i].doro_Site].P1_Status.handCards[k]
                                            if str(mylist[i].DeckDict["種類"][str(num)]).find("陷阱") == -1:
                                                   continue
                                            options.append(create_select_option(str(mylist[i].DeckDict["名稱"][str(num)]), value="select_trap_card_"+str(num), emoji="🥼"))
                                        if len(options) >1:
                                            select = create_select(options,
                                                                   custom_id='show_wand_selectCard',
                                                                   placeholder="這是你手上的卡",  # the placeholder text to show when no options have been chosen
                                                                   min_values=1,  # the minimum number of options a user must select
                                                                   max_values=1  # the maximum number of options a user can select
                                                                            )
                                        
                                            buttons = [         
                                            create_button(                                                         
                                                    label="返回",
                                                    style=ButtonStyle.primary,
                                                    custom_id="return_menu")
                                                    ]
                                            await ctx.edit_origin(content='你選擇的種類卡',components=[create_actionrow(select),create_actionrow(*buttons)],hidden=True)
                                            return
                                        
                                        
                                elif DoroSiteList[mylist[i].doro_Site].P2_Status.id == ctx.author_id:
                                    if len(DoroSiteList[mylist[i].doro_Site].P2_Status.handCards) !=0:
                                        options=[create_select_option('請選擇', value="select_trap_card_None", emoji="🥼")]
                                        for k in range(0,len(DoroSiteList[mylist[i].doro_Site].P2_Status.handCards)):
                                            num = DoroSiteList[mylist[i].doro_Site].P2_Status.handCards[k]
                                            if str(mylist[i].DeckDict["種類"][str(num)]).find("陷阱") == -1:
                                                   continue
                                            options.append(create_select_option(str(mylist[i].DeckDict["名稱"][str(num)]), value="select_trap_card_"+str(num), emoji="🥼"))
                                        if len(options) >1:
                                            select = create_select(options,
                                                                   custom_id='show_wand_selectCard',
                                                                   placeholder="你選擇的種類卡",  # the placeholder text to show when no options have been chosen
                                                                   min_values=1,  # the minimum number of options a user must select
                                                                   max_values=1  # the maximum number of options a user can select
                                                                            )
                                            
                                            buttons = [         
                                            create_button(                                                         
                                                    label="返回",
                                                    style=ButtonStyle.primary,
                                                    custom_id="return_menu")
                                                    ]
                                            await ctx.edit_origin(content='你選擇的種類卡',components=[create_actionrow(select),create_actionrow(*buttons)],hidden=True)
                                            return
                                   
                                await ctx.edit_origin(content='你手上沒有陷阱卡')
                                return
                            elif custom_id =='leave':
                                Card_Choices.pop(i)
                                upload(Card_Choices)
                                await ctx.send(mylist[i].name +" 離開決鬥")
                                mylist.pop(i)
                                return
                                return
                            
                            elif custom_id.find('monsterpoint') !=-1:
                                #0 表側攻擊表示
                                #1 表側防禦表示
                                #2 裏側攻擊表示
                                #3 裏側防禦表示
                                num = -1
                                ctype = -1
                                selectSplit = custom_id.split('_')
                                carid = selectSplit[0].replace('id-','')
                                num = selectSplit[2].replace('monsterpoint','')
                                if selectSplit[1] =='attckshow':
                                        ctype=0
                                elif selectSplit[1] =='defenshow':
                                        ctype =1
                                elif selectSplit[1] =='attckhide':
                                        ctype = 2
                                elif selectSplit[1] =='defenshide':
                                        ctype =3
                                    
                                if DoroSiteList[mylist[i].doro_Site].P1_Status.id == ctx.author_id:
                                    
                                    DoroSiteList[mylist[i].doro_Site].Site[0][int(num)].append(carid)
                                    DoroSiteList[mylist[i].doro_Site].Site[0][int(num)].append(ctype)
                                    for hand in range(0,len(DoroSiteList[mylist[i].doro_Site].P1_Status.handCards)):
                                        print(carid)
                                        print(DoroSiteList[mylist[i].doro_Site].P1_Status.handCards[hand])
                                        if carid == str(DoroSiteList[mylist[i].doro_Site].P1_Status.handCards[hand]): 
                                            print("執行")
                                            DoroSiteList[mylist[i].doro_Site].P1_Status.handCards.pop(hand)
                                            break
                                            
                                    await redorofun(ctx, DoroSiteList[mylist[i].doro_Site].P1_Status.health)
                            
                                elif DoroSiteList[mylist[i].doro_Site].P2_Status.id == ctx.author_id:
                                    
                                    DoroSiteList[mylist[i].doro_Site].Site[1][int(num)].append(carid)
                                    DoroSiteList[mylist[i].doro_Site].Site[1][int(num)].append(ctype)
                                    for hand in range(0,len(DoroSiteList[mylist[i].doro_Site].P2_Status.handCards)):
                                        print(carid)
                                        print(DoroSiteList[mylist[i].doro_Site].P2_Status.handCards[hand])
                                        if carid == str(DoroSiteList[mylist[i].doro_Site].P2_Status.handCards[hand]):
                                            print("執行")
                                            DoroSiteList[mylist[i].doro_Site].P2_Status.handCards.pop(hand)
                                            break
                                    
                                    await redorofun(ctx, DoroSiteList[mylist[i].doro_Site].P2_Status.health)
                                
                                return
                            elif custom_id.find('attckshow') !=-1:
                                button = [  ]
                                
                                selectSplit = custom_id.split('_')
                                
                                carid = selectSplit[0].replace('id-','')
                                if DoroSiteList[mylist[i].doro_Site].P1_Status.id == ctx.author_id:
                                    
                                    for search_site in range(0,5):
                                        
                                        if len(DoroSiteList[mylist[i].doro_Site].Site[0][search_site]) !=0:
                                            continue
                                        else:
                                            button.append(create_button(
                                                                    label='位置'+str(search_site),
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="id-"+carid+"_attckshow_monsterpoint"+str(search_site)),)
                                            
                                elif DoroSiteList[mylist[i].doro_Site].P2_Status.id == ctx.author_id:
                                    for search_site in range(0,5):
                                        
                                        if len(DoroSiteList[mylist[i].doro_Site].Site[1][search_site]) !=0:
                                            continue
                                        else:
                                            button.append(create_button(
                                                                    label='位置'+str(search_site),
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="id-"+carid+"_attckshow_monsterpoint"+str(search_site)),)
                                            
                                button2 = [ create_button(                                                         
                                                    label="返回",
                                                    style=ButtonStyle.primary,
                                                    custom_id="return_menu") 
                                    ]            
                                components = create_actionrow(*button)
                                await ctx.edit_origin(content="選擇卡片 位置",components=[components,create_actionrow(*button2)])
                                
                                return
                            
                            
                            
                            elif custom_id =='defenshide':
                                
                                button = [  
                                                        create_button(
                                                                    label='位置1',
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="monster_point_1"),
                                                        create_button(
                                                                    label='位置2',
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="monster_point_2"),
                                                        create_button(
                                                                    label='位置3',
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="monster_point_3"),
                                                        create_button(
                                                                    label='位置4',
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="monster_point_4"),
                                                        create_button(
                                                                    label='位置5',
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="monster_point_5"),
                                                        
                                                    ]
                                button2 = [ create_button(                                                         
                                                    label="返回",
                                                    style=ButtonStyle.primary,
                                                    custom_id="return_menu") 
                                    ]       
                                components = create_actionrow(*button)
                                
                                await ctx.edit_origin(content="選擇卡片 位置",components=[components,create_actionrow(*button2)])
                                
                                return
                                
                            
                            elif custom_id =='return_menu':
                                if DoroSiteList[mylist[i].doro_Site].P1_Status.id == ctx.author_id:
                                    await redorofun(ctx,DoroSiteList[mylist[i].doro_Site].P1_Status.health)
                                    return
                                elif DoroSiteList[mylist[i].doro_Site].P2_Status.id == ctx.author_id:
                                    await redorofun(ctx,DoroSiteList[mylist[i].doro_Site].P2_Status.health)
                                    return
                                    
                                
                            elif custom_id =='startAtk':
                                button = [  ]
                                
                                selectSplit = custom_id.split('_')
                                
                                carid = selectSplit[0].replace('id-','')
                                if DoroSiteList[mylist[i].doro_Site].P1_Status.id == ctx.author_id:
                                    for search_site in range(0,5):
                                        
                                        if len(DoroSiteList[mylist[i].doro_Site].Site[0][search_site]) !=0:
                                            if DoroSiteList[mylist[i].doro_Site].Site[0][search_site][1] == 0:
                                                button.append(create_button(    
                                                                            label=mylist[i].DeckDict['名稱'][DoroSiteList[mylist[0].doro_Site].Site[0][search_site][0]],
                                                                            style=ButtonStyle.primary,
                                                                            custom_id="id-"+DoroSiteList[mylist[i].doro_Site].Site[0][search_site][0]+"_怪獸"+str(search_site)),)
                                    if len(button) == 0:
                                        await ctx.edit_origin(content="你沒有可以攻擊的怪獸卡")
                                        return
                                    components = create_actionrow(*button)
                                    await ctx.edit_origin(content="選擇卡片 位置",components=[components])
                                    return
                                elif DoroSiteList[mylist[i].doro_Site].P2_Status.id == ctx.author_id:
                                    for search_site in range(0,5):
                                        if len(DoroSiteList[mylist[i].doro_Site].Site[1][search_site]) !=0:
                                            if DoroSiteList[mylist[i].doro_Site].Site[1][search_site][1] == 0:
                                                button.append(create_button(
                                                                        label=mylist[i].DeckDict['名稱'][DoroSiteList[mylist[0].doro_Site].Site[1][search_site][0]],
                                                                        style=ButtonStyle.primary,
                                                                        custom_id="id-"+DoroSiteList[mylist[i].doro_Site].Site[1][search_site][0]+"_怪獸"+str(search_site)),)
                                    if len(button) == 0:
                                        await ctx.edit_origin(content="你沒有可以攻擊的怪獸卡")
                                        return
                                    components = create_actionrow(*button)
                                    await ctx.edit_origin(content="選擇卡片 位置",components=[components])
                                    return
                            
            await ctx.send("你未開始決鬥，請先加入決鬥",hidden=True)
            

        @slash.component_callback()
        async def show_wand_selectCard(ctx: ComponentContext):
            custom_id = ctx.custom_id
            myid = ctx.author_id
            own = -1
            button = []
            selected_option = str(ctx.selected_options[0])
         
            if len(mylist) !=0 :
                    for i in range(len(mylist)):
                        if mylist[i].id == myid:
                            if selected_option.find('None') !=-1:
                                    await ctx.edit_origin(content="請選擇")
                                    return
                            elif selected_option.find('select_monster_card_') != -1:
                                
                                cardId = selected_option.replace('select_monster_card_','')
                                if mylist[i].DeckDict['種類'][cardId] == '效果怪獸' or mylist[i].DeckDict['種類'][cardId] == '通常怪獸':
                                    button = [  
                                                        create_button(
                                                                    label='表側攻擊表示',
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="id-"+cardId+"_attckshow"),
                                                        create_button(
                                                                    label='裏側防禦表示',
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="id-"+cardId+"_defenshide"),
                                                        create_button(                                                         
                                                                    label="返回",
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="return_menu")
                                                    ]
                                            
                                    components = create_actionrow(*button)
                                    await ctx.edit_origin(content="你選擇 怪獸卡 "+mylist[i].DeckDict['名稱'][cardId],components=[components])
                                
                                return
                            elif selected_option.find('select_magic_card_') !=-1:
                                button = [  
                                                        create_button(
                                                                    label='使用',
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="use_show"),
                                                        create_button(                                                         
                                                                    label="返回",
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="return_menu")
                                                    ]
                                            
                                components = create_actionrow(*button)
                                await ctx.edit_origin(content="你選擇 魔法卡 "+mylist[i].DeckDict['名稱'][cardId],components=[components])
                            elif selected_option.find('select_trap_card_') !=-1:
                                button = [  
                                                        create_button(
                                                                    label='覆蓋',
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="use_hide"),
                                                        create_button(                                                         
                                                                    label="返回",
                                                                    style=ButtonStyle.primary,
                                                                    custom_id="return_menu")
                                                    ]
                                            
                                components = create_actionrow(*button)
                                await ctx.edit_origin(content="你選擇 陷阱卡 "+mylist[i].DeckDict['名稱'][cardId],components=[components])
                                
                       
        async def dorofun (ctx,health):
                buttons = [
                            create_button(
                                           label="動作",
                                           style=ButtonStyle.primary,
                                           custom_id="action"),
                            
                            create_button(
                                           label="顯示手牌!!!",
                                           style=ButtonStyle.primary,
                                           custom_id="Show_handCards"),
                            create_button(
                                           label="顯示墓地卡片!!!",
                                           style=ButtonStyle.primary,
                                           custom_id="Show_GraveCards")
                            ]
                components = create_actionrow(*buttons)
                await ctx.send(content="生命值 : " + str(health),components=[components],hidden=True)
                                
                
        async def redorofun (ctx,health):
                buttons = [
                            create_button(
                                           label="動作",
                                           style=ButtonStyle.primary,
                                           custom_id="action"),
                            
                            create_button(
                                           label="顯示手牌!!!",
                                           style=ButtonStyle.primary,
                                           custom_id="Show_handCards"),
                            create_button(
                                           label="顯示墓地卡片!!!",
                                           style=ButtonStyle.primary,
                                           custom_id="Show_GraveCards")
                            ]
                components = create_actionrow(*buttons)
                await ctx.edit_origin(content="生命值 : " + str(health),components=[components],hidden=True)

        async def is_action (ctx,health,num):
            

            if num == 0:
                buttons = [
                            create_button(
                                           label="選擇卡片",
                                           style=ButtonStyle.primary,
                                           custom_id="select_card"),
                            create_button(
                                           label="攻擊宣言",
                                           style=ButtonStyle.primary,
                                           custom_id="startAtk"),
                            create_button(
                                           label="結束回合!!!",
                                           style=ButtonStyle.primary,
                                           custom_id="finish_turn"),
                            create_button(
                                           label="返回",
                                           style=ButtonStyle.primary,
                                           custom_id="return_menu")
                            ]
            else:
                
                buttons = [
                            create_button(
                                           label="抽卡!!!",
                                           style=ButtonStyle.primary,
                                           custom_id="doro")
                            ]
            components = create_actionrow(*buttons)
            await ctx.edit_origin(content="生命值 : " + str(health),components=[components],hidden=True)
        
        
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
                            
                        