# -*- coding: utf-8 -*-
import requests

class upload():
    def __init__(self, Card_Choices):
        self.Card_Choices = Card_Choices
        url = "https://discord.com/api/v8/applications/app_id/guilds/guild_id/commands"
        
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
            "Authorization": "Bot token"
        }
        
        
        
        r = requests.post(url, headers=headers, json=json)
        print(r)



    
