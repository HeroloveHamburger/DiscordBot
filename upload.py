# -*- coding: utf-8 -*-
import requests



class upload():
    def __init__(self, Card_Choices):
        self.Card_Choices = Card_Choices
        url = "https://discord.com/api/v8/applications/913237725195419658/guilds/730024186852147240/commands"
        
        # This is an example USER command, with a type of 2
        json = {
            "name": "attack",
            "type": 1,
            "description": "攻擊",
            "options": [
                {
                    "name": "who",
                    "description": "要攻擊誰",
                    "type": 3,
                    "required": True,
                    "choices": self.Card_Choices,
                    
                }
            ]
        }
        
        # For authorization, you can use either your bot token
        headers = {
            "Authorization": "Bot OTEzMjM3NzI1MTk1NDE5NjU4.YZ7k6A.foEd4rLyVS8SsNvLXZI_XO1sK5c"
        }
        
        
        
        r = requests.post(url, headers=headers, json=json)
        #print(r)
        # This is an example USER command, with a type of 2
        json = {
            "name": "challenge",
            "type": 1,
            "description": "發起挑戰",
            "options": [
                {
                    "name": "who",
                    "description": "對誰挑戰",
                    "type": 3,
                    "required": True,
                    "choices": self.Card_Choices,
                    
                }
            ]
        }
        
        # For authorization, you can use either your bot token
        headers = {
            "Authorization": "Bot OTEzMjM3NzI1MTk1NDE5NjU4.YZ7k6A.foEd4rLyVS8SsNvLXZI_XO1sK5c"
        }
        
        
        
        r = requests.post(url, headers=headers, json=json)
        #print(r)

