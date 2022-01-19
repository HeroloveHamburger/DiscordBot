# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
from selenium.webdriver.common.keys import Keys
import discord
import nest_asyncio
from discord.ext import commands 


nest_asyncio.apply()

intents=discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True

bot = commands.Bot(command_prefix='test',intents = intents)

@bot.event
async def on_ready():
    temp = "";
    channel = bot.get_channel(898497922226860033)
    print(">>Bot is online <<")
    
    
async def check():
    while (True):
        try:
            i = browser.execute_script(valueScript);
            if temp != i:
                temp = i
                await channel.send(temp)
                await print(i)
        except NoSuchElementException as aaa:
            browser.get("https://haha.gamer.com.tw/?room=60076")
            while (True):
                #嘗試執行該程式碼
                try:
                    browser.find_element_by_id("msg_input")
                    break
                #如果失敗
                except NoSuchElementException as e:
                    #等待一秒
                    sleep(1)
                    await print("wait")
    
browser = webdriver.Chrome()

browser.minimize_window()
    
browser.get("https://haha.gamer.com.tw/?room=60076")
    
browser.find_element_by_name("userid").send_keys("a850913")
    
browser.find_element_by_name("password").send_keys("870512day")
    
browser.find_element_by_id("btn-login").click()
    
testScript = ['Readword = ""; function timeFormat(timestamp, type) {if (timestamp == 0) {return ""} var now = new Date; var a = new Date(timestamp);var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];var year = a.getFullYear();var now_year = now.getFullYear();var month = a.getMonth() + 1;var now_month = now.getMonth() + 1;var date = a.getDate();var now_date = now.getDate();var hour = a.getHours();var min = a.getMinutes();'
                  +'var sec = a.getSeconds();if (month < 10) {month = "0" + month}if (date < 10) {date = "0" + date}if (now_month < 10) {now_month = "0" + now_month}if (now_date < 10) {now_date = "0" + now_date}if (hour < 10) {hour = "0" + hour}if (min < 10) {min = "0" + min}if (sec < 10) {sec = "0" + sec}switch (type) {case "log":var time = year + "/" + month + "/" + date + " " + hour + ":" + min + ":" + sec;break;case "note":var time = month + "/" + date + " " + hour + ":" + min;break;case "sticker":var time = year + "/" + month + "/" + date;break;case "sticker_dealine":var time = year + "年" + month + "月" + date + "日";break;case "sys_msg":var time = year + "/" + month + "/" + date + " " + hour + ":" + min;break;case "sys":var time = year + month + date;break;case "sys_show":var time = year + "年" + month + "月" + date + "日";break;case "ad":var time = now_year + "" + now_month + "" + now_date;break;default:var time = hour + ":" + min;break}return time};'
                  +'firebase.database().ref("im/database/info/60076/messages").orderByChild("timestamp").limitToLast(30).on("child_added", function(message) { '
                  +'var data = message.val(); '
                  +'if(data.sticker_group_id != undefined)'
                  +'{'
                  
                  +'Readword = data.sender_id +"|" + data.sender_name +": https://im.bahamut.com.tw/sticker%2F"+data.sticker_group_id+"%2F"+data.sticker_id+".png? ||時間" + timeFormat(data.timestamp,"log");'
                  +'}else if(data.image_id != undefined)'
                  +'{'
                  +'Readword = data.sender_id +"|" + data.sender_name +": https://im.bahamut.com.tw/chatimg%2F"+data.image_id+"."+data.image_ext+"? ||時間" + timeFormat(data.timestamp,"log");'
                  +'}else{'
                  +'Readword = data.sender_id +"|" + data.sender_name +":" + data.message + "  ||時間" + timeFormat(data.timestamp,"log");'
                  +'}'
                  +'})']
    
while (True):
    #嘗試執行該程式碼
    try:
        browser.find_element_by_id("msg_input")
        break
    #如果失敗
    except NoSuchElementException as e:
        #等待一秒
        sleep(1)
        print("wait")
    
browser.execute_script(testScript[0]);

    
valueScript = 'return Readword';
    
    
    
    
                    

bot.run("OTEzMjM3NzI1MTk1NDE5NjU4.YZ7k6A.8F95gaOh0Rge1osCXvMhJHqLlsw")