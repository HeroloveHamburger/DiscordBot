# -*- coding: utf-8 -*-
import random
class Player_Status():
    def __init__(self, id,name, health = 4000,cardNum = 40):
        self.status ={
            id :{'name' : name,
                'health' : health,
                'Deck' : "",
                'DeckDict' : [],
                'cardNum' : cardNum,
                'cardDict' : [],
                'cardDictGrave' : [],
                'challengBool' : False,
                'challenge_Name' : "",
                'challenge_id' : 0,
                'challenge_Author' : [],
                'doroStart' : False,
                'handCards' : [],
                'doro_Site' : -1,
                'first_doro' : False,
                'is_doro' : 1,
                'turn' : False,
                'site':-1,
                'selectCardName': '',
                'atk':0,
                'def':0
                }
            
            }
        
        
        


class Doro_Site():
    def __init__(self):
        # 0 = P1回合 1 = P2回合
        self.turn = random.randint(0, 1)
        self.Site = [[[],[],[],[],[],[],[],[],[],[]],
                     [[],[],[],[],[],[],[],[],[],[]]]
        
        
        #0 表側攻擊表示
        #1 表側防禦表示
        #3 裏側攻擊表示
        #4 裏側防禦表示