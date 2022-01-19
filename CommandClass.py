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
        
        @bot.event
        async def on_component(ctx:ComponentContext):
            custom_id = ctx.custom_id
            myid = str(ctx.author_id)
            own = -1
            button = []
            mname = ctx.author.name+"#"+ctx.author.discriminator
            #顯示決鬥者
            if custom_id == 'Number_of_duels':
                await ctx.send("目前"+str(len(mylist)) +"位")
                return            
            #加入決鬥
            elif custom_id =='join_duel':
                try:
                    mylist[myid]
                    await ctx.edit_origin(content= mname+"已經加入過",hidden=True)
                except:
                    player = Player_Status(myid,name=mname)
                    mylist.update(player.status)
                    Card_Choices.append(create_choice(name=mname,
                                    value= myid
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
                    
                return
            #選擇可用排組
            if custom_id.find('Select_Deck_doro') !=-1:
                deck = custom_id.replace('Select_Deck_doro','')
                mylist[myid]['Deck'] = deck
                print('./套牌/'+deck+'.json')
                with open('./套牌/'+deck+'.json','r',encoding="utf8") as jfile:
                        DeckDictdata = json.load(jfile)
                mylist[myid]['DeckDict'] = DeckDictdata
                #卡片順序
                mylist[myid]['cardDict'] = random.sample(range(0,len(DeckDictdata['名稱'])-1), len(DeckDictdata['名稱'])-1)
                mylist[myid]['cardNum'] = len(DeckDictdata['名稱'])
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
            #挑戰按鈕
            elif custom_id =='Challenge' :
                for k in mylist.keys():
                    if k==myid :
                        continue
                    button.append(create_button(
                    label=mylist[k]['name'],
                    style=ButtonStyle.primary,
                    custom_id="Challenge_to"+str(k)))
                    components = create_actionrow(*button)
                if len(button) !=0:
                    await ctx.edit_origin(content="可選擇的挑戰對象",components=[components],hidden=True) 
                else:
                    await ctx.edit_origin(content="無人可挑戰",hidden=True) 
                return
            #對誰挑戰
            elif custom_id.find('Challenge_to') !=-1 :
                who = custom_id.replace('Challenge_to','')
                if ctx.author_id == int(who):
                    await ctx.edit_origin(content="不可以對自己挑戰")
                    return

                if len(mylist[myid]['DeckDict']) ==0:
                    await ctx.edit_origin(content="<@!"+str(myid)+"> 請先選擇套牌，在發起挑戰")
                    return
                        

                if len(mylist[who]['DeckDict']) ==0:
                    await ctx.edit_origin(content="對方尚未選擇套牌，無法挑戰")
                    return
                #自己
                buttons = [
                            create_button(
                                           label="接受!!!",
                                           style=ButtonStyle.primary,
                                           custom_id="Accept"+str(who)),
                                        create_button(
                                           label="拒絕!!!",
                                           style=ButtonStyle.primary,
                                           custom_id="UnAccept"),
                                            
                          ]
                components = create_actionrow(*buttons)
                await ctx.send("<@!"+str(who)+"> \n"+mylist[myid]['name']+"對你發起挑戰\n要接受嗎?",components=[components])
                mylist[who]['challengBool'] = True
                mylist[who]['challenge_Author'] = ctx.author
                mylist[who]['challenge_Name'] = str(mylist[myid]['name'])
                mylist[who]['challenge_id'] = myid
                #print(mylist[who]['challenge_id'] + " : "+ myid)
                mylist[myid]['challengBool'] = True
                mylist[myid]['challenge_Name'] =  str(mylist[who]['name'])
                mylist[myid]['challenge_id'] =  str(who)
                #print(mylist[myid]['challenge_id'] + " : "+ who)
                return
            #接受挑戰
            elif custom_id.find('Accept') !=-1 :
                who = custom_id.replace('Accept','')
                #print(who+" : "+ mylist[who]['challenge_id'])
                #print(mylist[myid]['challenge_id'] + " : " +myid )
                
                if myid == who :
                    
                    mylist[myid]['doroStart'] = True
                    mylist[mylist[myid]['challenge_id']]['doroStart'] = True
                    
                    mylist[myid]['doro_Site'] = len(DoroSiteList)
                    mylist[mylist[myid]['challenge_id']]['doro_Site'] = len(DoroSiteList)
                    
                    DoroSiteList.append(Doro_Site())
                    
                    buttons = [
                        create_button(
                                       label="決鬥開始!!!",
                                       style=ButtonStyle.primary,
                                       custom_id="duel")
                      ]
                    components = create_actionrow(*buttons)
                    
                    await ctx.send("<@!"+str(mylist[myid]['challenge_id'])+"> \n"+mylist[myid]['name']+"以接受你的挑戰!\n",components =[components])
                    if DoroSiteList[mylist[myid]['doro_Site']].turn == 0:
                        mylist[myid]['turn'] = True
                        mylist[myid]['site'] = 0
                        mylist[mylist[myid]['challenge_id']]['turn'] = False
                        mylist[mylist[myid]['challenge_id']]['site'] = 1
                        await ctx.send("由<@!"+myid+"> 先攻")
                    else:
                        mylist[myid]['turn'] = False
                        mylist[myid]['site'] = 0
                        mylist[mylist[myid]['challenge_id']]['turn'] = True
                        mylist[mylist[myid]['challenge_id']]['site'] = 1
                        await ctx.send("由<@!"+str(mylist[myid]['challenge_id'])+"> 先攻")

                    return
                else:
                    await ctx.send("你無法使用此按鈕",hidden=True)
                    return
            #動作
            elif custom_id =='action':
                if mylist[myid]['doro_Site'] == -1:
                    await ctx.send("你沒有在決鬥場",hidden=True)
                    return
                await is_action(ctx,mylist[myid]['health'],mylist[myid]['is_doro'])
                
                return
            #初始抽排
            elif custom_id == 'duel':
                if mylist[myid]['doro_Site'] == -1:
                    await ctx.send("你沒有在決鬥場",hidden=True)
                    return
                
                if mylist[myid]['first_doro'] == True:
                    await ctx.edit_origin(content="你不能再抽五張卡")
                    return
                
                for kk in range(0,5):
                    #print(k)
                    mylist[myid]['cardNum'] = mylist[myid]['cardNum'] -1
                    mylist[myid]['handCards'].append(mylist[myid]['cardDict'][0])
                    mylist[myid]['cardDict'].pop(0)
                await ctx.send("<@!"+myid+">決鬥開始!!!\n抽五張牌")
                mylist[myid]['first_doro'] = True
                
                await dorofun(ctx,mylist[myid]['health'])
                return

            #一般抽牌
            elif custom_id == 'doro':
                
                if len(mylist[myid]['DeckDict']) ==0:
                    await ctx.edit_origin(content="找不到您使用的牌組")
                    return
                
                if mylist[myid]['turn'] != True:
                    await ctx.edit_origin(content="還不到你的回合，不能抽卡",hidden=True)
                    return
                if mylist[myid]['is_doro'] == 0:
                    await ctx.edit_origin(content="你已經抽過卡，請等下一回合",hidden=True)
                    return
                
                if mylist[myid]['cardNum'] ==0:
                    await ctx.edit_origin(content="你沒卡了",hidden=True)
                    return
                mylist[myid]['is_doro'] = mylist[myid]['is_doro'] -1
                mylist[myid]['cardNum'] = mylist[myid]['cardNum'] -1
                mylist[myid]['handCards'].append(mylist[myid]['cardDict'][0])
                
                await ctx.edit_origin(content="執行指令",components=[],hidden=True)
                await ctx.send(mylist[myid]['name'] + " 抽了一張卡")
            
                content = str("名稱 :"+mylist[myid]['DeckDict']['名稱'][str(mylist[myid]['cardDict'][0])] +
                               "\n"+
                               "種類 :"+mylist[myid]['DeckDict']['種類'][str(mylist[myid]['cardDict'][0])] +
                               "\n"+
                               "屬性 :"+mylist[myid]['DeckDict']['屬性'][str(mylist[myid]['cardDict'][0])] +
                               "\n"+
                               "等級 :"+mylist[myid]['DeckDict']['等級'][str(mylist[myid]['cardDict'][0])] +
                               "\n"+
                               "種族 :"+mylist[myid]['DeckDict']['種族'][str(mylist[myid]['cardDict'][0])] +
                               "\n"+
                               "攻擊 :"+mylist[myid]['DeckDict']['攻擊'][str(mylist[myid]['cardDict'][0])] +
                               "\n"+
                               "守備 :"+mylist[myid]['DeckDict']['守備'][str(mylist[myid]['cardDict'][0])] +
                               "\n"+
                               "效果 :"+mylist[myid]['DeckDict']['效果'][str(mylist[myid]['cardDict'][0])] )
                
                
                if mylist[myid]['DeckDict']['image_url'][str(mylist[myid]['cardDict'][0])] != '':
                    content = content + "\n" + mylist[myid]['DeckDict']['image_url'][str(mylist[myid]['cardDict'][0])]
                else:
                    content = content + "\n" + '沒有圖片'
                
                mylist[myid]['cardDict'].pop(0)
                await ctx.send(content,hidden=True)
                await dorofun(ctx,mylist[myid]['health'])
                return
                
                
            #顯示手上卡片    
            elif custom_id == 'Show_handCards':
                text=''
                if mylist[myid]['doro_Site'] == -1:
                    await ctx.send("你沒有在決鬥場",hidden=True)
                    return 

                if len(mylist[myid]['handCards']) !=0:
                    options=[]
                    for k in range(0,len(mylist[myid]['handCards'])):
                        num = mylist[myid]['handCards'][k]
                        options.append(create_select_option(str(mylist[myid]['DeckDict']["名稱"][str(num)]), value="show_selectCard_"+str(num), emoji="🥼"))
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

            #顯示墓地卡片
            elif custom_id =='Show_GraveCards':
                text=''
                if mylist[myid]['doro_Site'] == -1:
                    await ctx.send("你沒有在決鬥場",hidden=True)
                    return

                if len(mylist[myid]['cardDictGrave']) !=0:
                    for k in range(0,len(mylist[myid]['cardDictGrave'])):
                        num = mylist[myid]['handCards'][k]
                        options.append(create_select_option(str(mylist[myid]['DeckDict']["名稱"][str(num)]), value="show_selectCard_"+str(num), emoji="🥼"))
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
            #選擇卡片
            elif custom_id == 'select_card':
                    text=''
                    if mylist[myid]['doro_Site'] == -1:
                        await ctx.send("你沒有在決鬥場",hidden=True)
                        return
 
                    if len(mylist[myid]['handCards']) !=0:
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

            #結束回合
            elif custom_id =='finish_turn':
                    
                if len(mylist[myid]['DeckDict']) ==0:
                    await ctx.send("找不到您使用的牌組")
                    return
                
                if mylist[myid]['turn'] == False:
                    await ctx.send("還不到你的回合，不能結束",hidden=True)
                    await dorofun(ctx,mylist[myid]['health'])
                    return
                if mylist[myid]['is_doro'] >0:
                    await ctx.send("卡片能抽數量未抽完，不能結束",hidden=True)
                    await dorofun(ctx,mylist[myid]['health'])
                    return
                print('p1')
                mylist[myid]['is_doro'] = 1
                mylist[myid]['turn'] = False
                mylist[mylist[myid]['challenge_id']]['turn'] = True
                await ctx.send("<@!"+str(myid)+">回合結束!!!\n輪到<@!"+str(mylist[myid]['challenge_id'])+">回合")
                
                
                await dorofun(ctx,mylist[myid]['health'])
                return
                    
                    
                    

            #選擇怪獸卡
            elif custom_id =='monster_card':
                
                
            
                 if len(mylist[myid]['handCards']) !=0:
                    options=[create_select_option('請選擇', value="select_monster_card_None", emoji="🥼")]
                    for k in range(0,len(mylist[myid]['handCards'])):
                        num = mylist[myid]['handCards'][k]
                        if str(mylist[myid]['DeckDict']["種類"][str(num)]).find("怪獸") == -1:
                               continue
                        options.append(create_select_option(str(mylist[myid]['DeckDict']["名稱"][str(num)]), value="select_monster_card_"+str(num), emoji="🥼"))
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
                    else:

                    
                        await ctx.edit_origin(content='你手上沒有怪獸卡',hidden=True)
                        return
            #選擇魔法卡
            elif custom_id =='magic_card':
                
                if mylist[myid]['doro_Site'] == -1:
                    await ctx.send("你沒有在決鬥場",hidden=True)
                    return
                
                options=[create_select_option('請選擇', value="select_magic_card_None", emoji="🥼")]
                if len(mylist[myid]['handCards']) !=0:
                    
                    for k in range(0,len(mylist[myid]['handCards'])):
                        num = mylist[myid]['handCards'][k]
                        if str(mylist[myid]['DeckDict']["種類"][str(num)]).find("魔法") == -1:
                               continue
                        options.append(create_select_option(str(mylist[myid]['DeckDict']["名稱"][str(num)]), value="select_magic_card_"+str(num), emoji="🥼"))
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
                    else:
                 
                        await ctx.edit_origin(content='你手上沒有魔法卡',hidden=True)
                        return
            
            #選擇陷阱卡
            elif custom_id =='trap_card':
                
                if mylist[myid]['doro_Site'] == -1:
                    await ctx.send("你沒有在決鬥場",hidden=True)
                    return
                
                if len(mylist[myid]['handCards']) !=0:
                    options=[create_select_option('請選擇', value="select_trap_card_None", emoji="🥼")]
                    for k in range(0,len(mylist[myid]['handCards'])):
                        num = mylist[myid]['handCards'][k]
                        if str(mylist[myid].DeckDict["種類"][str(num)]).find("陷阱") == -1:
                               continue
                        options.append(create_select_option(str(mylist[myid]['DeckDict']["名稱"][str(num)]), value="select_trap_card_"+str(num), emoji="🥼"))
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
                        
                        

                   
                await ctx.edit_origin(content='你手上沒有陷阱卡')
                return
            #離開決鬥
            elif custom_id =='leave':
                Card_Choices.pop(i)
                upload(Card_Choices)
                await ctx.send(mylist[myid]['name'] +" 離開決鬥")
                mylist.pop(i)
                return
                return
            #放置怪獸卡到場片
            elif custom_id.find('_monsterpoint') !=-1:
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

                DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[myid]['site']][int(num)].append(carid)
                DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[myid]['site']][int(num)].append(ctype)
                for hand in range(0,len(mylist[myid]['handCards'])):
                    print(carid)
                    print(mylist[myid]['handCards'][hand])
                    if carid == str(mylist[myid]['handCards'][hand]): 
                        print("執行")
                        mylist[myid]['handCards'].pop(hand)
                        break
                        
                await redorofun(ctx, mylist[myid]['health'])
        

                
                return
            #表側攻擊表示
            elif custom_id.find('_attckshow') !=-1:
                button = [  ]
                
                selectSplit = custom_id.split('_')
                
                carid = selectSplit[0].replace('id-','')

                for search_site in range(0,5):
                    
                    if len(DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[myid]['site']][search_site]) !=0:
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
            
            
            #覆蓋怪獸卡並防禦
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
                
            #返回到主使用選下
            elif custom_id =='return_menu':
                await redorofun(ctx,mylist[myid]['health'])
                return
                
            #開始戰鬥
            elif custom_id =='startAtk':
                button = [  ]
                
                selectSplit = custom_id.split('_')
                
                carid = selectSplit[0].replace('id-','')
                for search_site in range(0,5):
                    
                    if len(DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[myid]['site']][search_site]) !=0:
                        print("id-"+DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[myid]['site']][search_site][0]+"_要攻擊的怪獸位置-"+str(search_site))
                        button.append(create_button(    
                                                    label=mylist[myid]['DeckDict']['名稱'][DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[myid]['site']][search_site][0]],
                                                    style=ButtonStyle.primary,
                                                    custom_id="id-"+DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[myid]['site']][search_site][0]+"_要攻擊的怪獸位置-"+str(search_site)),)
                if len(button) == 0:
                    await ctx.edit_origin(content="你沒有可以攻擊的怪獸卡")
                    return
                components = create_actionrow(*button)
                await ctx.edit_origin(content="選擇卡片 位置",components=[components])
                return
            #對方可以攻擊的怪獸位置
            elif custom_id.find('_要攻擊的怪獸位置') !=-1:
                button = [  ]
                
                selectSplit = custom_id.split('_')
                
                carid = selectSplit[0].replace('id-','')
                mylist[myid]['selectCardName'] = mylist[myid]['DeckDict']['名稱'][carid]
                mylist[myid]['atk'] = mylist[myid]['DeckDict']['攻擊'][carid]
                mylist[myid]['def'] = mylist[myid]['DeckDict']['守備'][carid]
                for search_site in range(0,5):
                    
                    if len(DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[mylist[myid]['challenge_id']]['site']][search_site]) !=0:
                        labelName = mylist[mylist[myid]['challenge_id']]['DeckDict']['名稱'][DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[mylist[myid]['challenge_id']]['site']][search_site][0]]
                        if DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[mylist[myid]['challenge_id']]['site']][search_site][1] == 0 :
                            button.append(create_button(
                                                    label=labelName,
                                                    style=ButtonStyle.primary,
                                                    custom_id="id-"+DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[mylist[myid]['challenge_id']]['site']][search_site][0]+"_被攻擊的怪獸-顯示攻擊"+str(search_site)),)
                            
                        elif DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[mylist[myid]['challenge_id']]['site']][search_site][1] == 1:
                            button.append(create_button(
                                                    label=labelName,
                                                    style=ButtonStyle.primary,
                                                    custom_id="id-"+DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[mylist[myid]['challenge_id']]['site']][search_site][0]+"_被攻擊的怪獸-顯示防禦"+str(search_site)),)
                        
                        elif DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[mylist[myid]['challenge_id']]['site']][search_site][1] == 2:
                            button.append(create_button(
                                                label='位置'+str(search_site),
                                                style=ButtonStyle.primary,
                                                custom_id="id-"+DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[mylist[myid]['challenge_id']]['site']][search_site][0]+"_被攻擊的怪獸-蓋牌攻擊"+str(search_site)),)
                        elif DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[mylist[myid]['challenge_id']]['site']][search_site][1] == 3:
                            button.append(create_button(
                                                label='位置'+str(search_site),
                                                style=ButtonStyle.primary,
                                                custom_id="id-"+DoroSiteList[mylist[myid]['doro_Site']].Site[mylist[mylist[myid]['challenge_id']]['site']][search_site][0]+"_被攻擊的怪獸-蓋牌防禦"+str(search_site)),)
                        
                        

                            
                button2 = [ create_button(                                                         
                                    label="返回",
                                    style=ButtonStyle.primary,
                                    custom_id="return_menu") 
                    ]            
                components = create_actionrow(*button)
                await ctx.edit_origin(content="選擇卡片 位置",components=[components,create_actionrow(*button2)])
                return
                            
            elif custom_id.find('_被攻擊的怪獸') !=-1:
                button = [  ]
                
                selectSplit = custom_id.split('_')
                print("-----------------------1")
                carid = selectSplit[0].replace('id-','')
                status = selectSplit[1].replace('被攻擊的怪獸-','')
                print("-----------------------2")
                mylist[mylist[myid]['challenge_id']]['selectCardName'] = mylist[mylist[myid]['challenge_id']]['DeckDict']['名稱'][carid]
                mylist[mylist[myid]['challenge_id']]['atk'] = mylist[mylist[myid]['challenge_id']]['DeckDict']['攻擊'][carid]
                mylist[mylist[myid]['challenge_id']]['def'] = mylist[mylist[myid]['challenge_id']]['DeckDict']['守備'][carid]
                print("-----------------------3")
                
                be_attacked = int(mylist[mylist[myid]['challenge_id']]['atk'])
                attacked = int(mylist[myid]['atk'])
                print(status)
                if status.find("顯示攻擊") !=-1:
                    if attacked > be_attacked :
                        print("-----------------------4")
                        dechealth = attacked - be_attacked
                        await ctx.send(mylist[mylist[myid]['challenge_id']]['selectCardName'] +"被 " +mylist[myid]['selectCardName'] + "打敗")
                        await ctx.send(mylist[myid]['challenge_Name'] +"遭受 " +mylist[myid]['name']+"<@!"+ctx.author.discriminator + "> "+ str(dechealth) + "點的攻擊")
                        mylist[mylist[myid]['challenge_id']]['health'] = mylist[mylist[myid]['challenge_id']]['health'] - dechealth
                    elif attacked < be_attacked :
                        print("-----------------------5")
                        dechealth = be_attacked - attacked
                        await ctx.send( mylist[myid]['selectCardName'] +"被 " +mylist[mylist[myid]['challenge_id']]['selectCardName']+ "打敗")
                        await ctx.send( mylist[myid]['name']+"遭受 " +mylist[myid]['challenge_Name']+"<@!"+mylist[myid]['challenge_id'] + "> "+ str(dechealth) + "點的攻擊")
                        mylist[myid]['health'] = mylist[myid]['health'] - dechealth
                    elif attacked == be_attacked :
                        print("-----------------------6")
                        await ctx.send( mylist[myid]['selectCardName'] +"跟 " +mylist[mylist[myid]['challenge_id']]['selectCardName']+ "互相傷害都死了")
                elif status.find("顯示防禦")!=-1:
                    if attacked > be_attacked :
                        print("-----------------------4")
                        dechealth = attacked - be_attacked
                        await ctx.send(mylist[mylist[myid]['challenge_id']]['selectCardName'] +"被 " +mylist[myid]['selectCardName'] + "打敗")
                        await ctx.send(mylist[myid]['challenge_Name'] +"遭受 " +mylist[myid]['name']+"<@!"+ctx.author.discriminator + "> "+ str(dechealth) + "點的攻擊")
                        mylist[mylist[myid]['challenge_id']]['health'] = mylist[mylist[myid]['challenge_id']]['health'] - dechealth
                    elif attacked < be_attacked :
                        print("-----------------------5")
                        dechealth = be_attacked - attacked
                        await ctx.send( mylist[myid]['selectCardName'] +"被 " +mylist[mylist[myid]['challenge_id']]['selectCardName']+ "打敗")
                        await ctx.send( mylist[myid]['name']+"遭受 " +mylist[myid]['challenge_Name']+"<@!"+mylist[myid]['challenge_id'] + "> "+ str(dechealth) + "點的攻擊")
                        mylist[myid]['health'] = mylist[myid]['health'] - dechealth
                    elif attacked == be_attacked :
                        print("-----------------------6")
                        await ctx.send( mylist[myid]['selectCardName'] +"跟 " +mylist[mylist[myid]['challenge_id']]['selectCardName']+ "互相傷害都死了")
                    
                elif status.find("蓋牌攻擊")!=-1:
                    if attacked > be_attacked :
                        print("-----------------------4")
                        dechealth = attacked - be_attacked
                        await ctx.send(mylist[mylist[myid]['challenge_id']]['selectCardName'] +"被 " +mylist[myid]['selectCardName'] + "打敗")
                        await ctx.send(mylist[myid]['challenge_Name'] +"遭受 " +mylist[myid]['name']+"<@!"+ctx.author.discriminator + "> "+ str(dechealth) + "點的攻擊")
                        mylist[mylist[myid]['challenge_id']]['health'] = mylist[mylist[myid]['challenge_id']]['health'] - dechealth
                    elif attacked < be_attacked :
                        print("-----------------------5")
                        dechealth = be_attacked - attacked
                        await ctx.send( mylist[myid]['selectCardName'] +"被 " +mylist[mylist[myid]['challenge_id']]['selectCardName']+ "打敗")
                        await ctx.send( mylist[myid]['name']+"遭受 " +mylist[myid]['challenge_Name']+"<@!"+mylist[myid]['challenge_id'] + "> "+ str(dechealth) + "點的攻擊")
                        mylist[myid]['health'] = mylist[myid]['health'] - dechealth
                    elif attacked == be_attacked :
                        print("-----------------------6")
                        await ctx.send( mylist[myid]['selectCardName'] +"跟 " +mylist[mylist[myid]['challenge_id']]['selectCardName']+ "互相傷害都死了")
                    
                elif status.find("蓋牌防禦")!=-1:
                    if attacked > be_attacked :
                        print("-----------------------4")
                        dechealth = attacked - be_attacked
                        await ctx.send(mylist[mylist[myid]['challenge_id']]['selectCardName'] +"被 " +mylist[myid]['selectCardName'] + "打敗")
                        await ctx.send(mylist[myid]['challenge_Name'] +"遭受 " +mylist[myid]['name']+"<@!"+ctx.author.discriminator +"> "+ str(dechealth) + "點的攻擊")
                        mylist[mylist[myid]['challenge_id']]['health'] = mylist[mylist[myid]['challenge_id']]['health'] - dechealth
                    elif attacked < be_attacked :
                        print("-----------------------5")
                        dechealth = be_attacked - attacked
                        await ctx.send( mylist[myid]['selectCardName'] +"被 " +mylist[mylist[myid]['challenge_id']]['selectCardName']+ "打敗")
                        await ctx.send( mylist[myid]['name']+"遭受 " +mylist[myid]['challenge_Name']+"<@!"+mylist[myid]['challenge_id'] + "> "+ str(dechealth) + "點的攻擊")
                        mylist[myid]['health'] = mylist[myid]['health'] - dechealth
                    elif attacked == be_attacked :
                        print("-----------------------6")
                        await ctx.send( mylist[myid]['selectCardName'] +"跟 " +mylist[mylist[myid]['challenge_id']]['selectCardName']+ "互相傷害都死了")
                
                return
            
            await ctx.send("你未開始決鬥，請先加入決鬥",hidden=True)
            

        @slash.component_callback()
        async def show_wand_selectCard(ctx: ComponentContext):
            custom_id = ctx.custom_id
            myid = str(ctx.author_id)
            own = -1
            button = []
            selected_option = str(ctx.selected_options[0])
         

            if selected_option.find('None') !=-1:
                    await ctx.edit_origin(content="請選擇")
                    return
            elif selected_option.find('select_monster_card_') != -1:
                
                cardId = selected_option.replace('select_monster_card_','')
                if mylist[myid]['DeckDict']['種類'][cardId] == '效果怪獸' or mylist[myid]['DeckDict']['種類'][cardId] == '通常怪獸':
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
                    await ctx.edit_origin(content="你選擇 怪獸卡 "+mylist[myid]['DeckDict']['名稱'][cardId],components=[components])
                
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
                await ctx.edit_origin(content="你選擇 魔法卡 "+mylist[myid]['DeckDict']['名稱'][cardId],components=[components])
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
                await ctx.edit_origin(content="你選擇 陷阱卡 "+mylist[myid]['DeckDict']['名稱'][cardId],components=[components])
                                
                       
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
                    if mylist[myid].id == ctx.author_id:
                        checkIsdoro = True
                        break
                    else:
                        checkIsdoro = False
                if checkIsdoro == False:
                    await ctx.send("你未參賽!!!請先/join_duel")
                    return
                for i in range(len(mylist)):
                    if mylist[myid].id == int(who):
                        if mylist[myid].health <0:
                            await ctx.send(str(mylist[myid].name) + "  已經葛屁了")
                            break
                        dechealth = random.randint(100,500)
                        await asyncio.sleep(1)
                        await ctx.send(str(mylist[myid].name) +"遭受 " +ctx.author.name+"#"+ctx.author.discriminator + " "+ str(dechealth) + "點的攻擊")
                        mylist[myid].health = mylist[myid].health - dechealth
                        if mylist[myid].health <0:
                            await ctx.send(str(mylist[myid].name) + "  葛屁了")
                            break
                        await ctx.send("剩下"+str(mylist[myid].health))
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
                            
                        