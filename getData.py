# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from time import sleep



def addCard(id,name,type,Attributes,Level,Race,atk,defense,Effect,image_url):
    dict = {  
        "id": id,
        "名稱":name,
        "種類":type,
        "屬性": Attributes,
        "等級": Level,
        "種族": Race,
        "攻擊": atk,
        "守備": defense,
        "效果":Effect,
        "image_url":image_url
    }
    return dict


for num in range (1,16):

    fileName = 'Vol'+str(num)+'.json'
    idnum = 327 + num
    html_doc = requests.get('https://asia.xpg.cards/pack?id='+ str(idnum))
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    
    cardListMenu = soup.find(id='__NEXT_DATA__')
    
    
    cardListMenu = str(cardListMenu).replace('<script id="__NEXT_DATA__" type="application/json">','')
    
    cardListMenu = cardListMenu.replace('</script>', '')
    
    
    cardListMenuJson = json.loads(cardListMenu)
    mydict =[]
    for key in cardListMenuJson['props']['apolloState'].keys():
            if str(key).find('Pack') !=-1 or str(key).find('ROOT_QUERY') !=-1:
                continue
            cardValue = requests.get("https://asia.xpg.cards/card?id="+
                                     cardListMenuJson['props']
                                     ['apolloState']
                                     [key]
                                     ['serialNumber'])
            
            cardsoup = BeautifulSoup(cardValue.text, 'html.parser')
            
            cardName = cardsoup.find(class_='sc-1gro38-2 legjSx mt-3 mt-md-0').text
            print(cardName)
            
            cardSkill = cardsoup.find(class_='sc-1gro38-1 kjwPDM')
            
            
            cardSkillLi= cardSkill.findAll('li')
            cardSkilldict = []
            for i in range(len(cardSkillLi)):
                cardSkillSplit = cardSkillLi[i].text.split('\xa0\xa0')
                print(cardSkillSplit[0] +":" + cardSkillSplit[1])
                cardSkilldict.append(cardSkillSplit[1])
            
            cardEffect = cardsoup.find(class_='sc-1gro38-4 hfjWSp mt-3 p-3').text
            
            print(cardEffect)
            
            cardImg = cardsoup.find(class_='sc-1gro38-3 dsQTGY p-0')
            
            if str(cardImg.attrs['src']).find('null') !=-1:
                cardImg.attrs['src'] = ''
            
            mydict.append(addCard(str(key).split(":")[1],
                                  cardName,
                                  cardSkilldict[0],
                                  cardSkilldict[1],
                                  cardSkilldict[2],
                                  cardSkilldict[3],
                                  cardSkilldict[4],
                                  cardSkilldict[5],
                                  cardEffect.replace('\r\n',''),
                                  cardImg.attrs['src']))
                
    df = pd.DataFrame(mydict)
    df.to_json(fileName,force_ascii=False)


