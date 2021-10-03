class Card:                     #卡牌类
    def __init__(self,sum=0):
        self.sum = sum
        self.card = []

class Card_zu(Card):            #卡组类
    def __init__(self):
        super().__init__()
        self.sum=52                                                                             #卡组卡牌数
        self.card=['S1','S2','S3','S4','S5','S6','S7','S8','S9','S10','SJ','SQ','SK',
                   'H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','HJ','HQ','HK',
                   'C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','CJ','CQ','CK',
                   'D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','DJ','DQ','DK',]           #卡组组成

    def Updata_Card_zu(self,card):                                                               #更新卡组
        if card in self.card:
            self.card.pop(self.card.index(card))
            self.sum=self.sum-1

class Placement_Area(Card):                                                                     #放置区类
    def Put_in(self,card):                                                                      #放入卡牌
        self.card.append(card)
        self.sum=len(self.card)

    def  Whether_Eat_Cards(self):                                                               #判断是否吃牌
        if self.sum>=2:
            return self.card[sum-1]==self.card[sum-2]
        else:
            return False

    def Empty_Card(self):                                                                       #放置区清零
        self.card.clear()
        self.sum=len(self.card)

class Player(Card):                                                                             #玩家类
    def __init__(self,name):
        super(Player, self).__init__()
        self.name=name

    def Update_Player_Card(self,Card):
        if card in self.card:
            self.card.pop(self.card.index(card))
            self.sum=self.sum-1

    def Knockout(self):         #打出手牌
        self.sum -= 1
        print("当前手牌数为：%d"%len(self.card))
        for card in self.card:
            print(card,end=' ')
        Brand = int(input('\n请输入要打出的牌号:'))
        return self.card.pop(Brand-1)

    def Eat_Cards(self,Place_Area):#吃牌
        print(self.name,"吃牌")
        for card in Place_Area.card:
            self.card.append(card)
        Place_Area.Empty_Card()
        self.sum = len(self.card)


