import random
import uuid


class Player:
    
    def __init__(self,players,money,pns):
        self.ids =["player 1", "player 2", "player 3", "player 4", "player 5"]
        self.players = players
        self.money = money
        self.pns = pns
        
        
    def player_divider(self) -> dict:
        # it will devide 5 peopele to 
        # four is contributor and one is judge
        # all the player will get revenue or benifit
        # and then it will return dict 
        if self.players > 0 and self.players <= 5:
            contributers = random.sample(self.ids,4)
            judge = [player for player in self.ids if player not in contributers][0]