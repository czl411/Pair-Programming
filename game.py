import random as r

class Card:                     #卡牌类
    def __init__(self,sum=0):
        self.sum = sum
        self.card = []

class Card_zu(Card):            #卡组类
    def __init__(self):
        super().__init__()
        self.sum=16                             #卡组卡牌数
        self.card=['♠','♥','♣','♦']*4           #卡组组成

    def random_card(self):
        self.sum -= 1
        return self.card.pop(r.randint(0,self.sum))

class Placement_Area(Card):     #放置区类

    def Put_in(self,card):      #放入卡牌
        self.card.append(card)
        self.sum=len(self.card)

    def Empty_Card(self):       #放置区清零
        self.card.clear()
        self.sum=len(self.card)

class Player(Card):             #玩家类
    def __init__(self,name):
        super(Player, self).__init__()
        self.name=name

    def Knockout(self):         #打出手牌
        self.sum -= 1
        print("当前手牌数为：%d"%len(self.card))
        for card in self.card:
            print(card,end=' ')
        Brand = int(input('\n请输入要打出的牌号:'))
        return self.card.pop(Brand-1)

    def Touch_Card(self,Card_Group):#摸牌
        get_card = Card_Group.random_card()
        return get_card

    def Eat_Cards(self,Place_Area):#吃牌
        print(self.name,"吃牌")
        for card in Place_Area.card:
            self.card.append(card)
        Place_Area.Empty_Card()
        self.sum = len(self.card)

class Game_Rule:                    #游戏规则类
    def __init__(self):
        self.Game_Start = 1
        self.Gameing = 0
    def Whether_Eat_Cards(self,What_Card,Place_Area): #判断是否吃牌
        if Place_Area.sum:
            if What_Card == Place_Area.card[Place_Area.sum-1]:
                return 1
        return 0

def Put_Place_Area(Place_Area,Game,card,who):   #放入放置区，并判断是否执行吃牌
    if Place_Area.sum:  # 放置区不为空
        if Game.Whether_Eat_Cards(card, Place_Area):  # 判断是否吃牌
            Place_Area.Put_in(card)  # 先放入
            P[who].Eat_Cards(Place_Area)  # P[who]吃牌
        else:
            Place_Area.Put_in(card)  # 放入放置区
    else:
        Place_Area.Put_in(card)  # 放入放置区
'''
初始化，加载游戏内容
'''
Game = Game_Rule()
P = []
P.append(Player("陈志良"))
P.append(Player("李知恩"))

Cards = Card_zu()
print(Cards.sum)
Place_Area = Placement_Area()
who = 0
while Cards.sum != 0:
    if P[who].sum == 0:                      #手上没牌
        print("%s手上没牌！"%P[who].name)
        card = P[who].Touch_Card(Cards)    #P1摸牌
        print("%s摸到了"%P[who].name,card)
        print("卡组剩余：", Cards.sum)
        Put_Place_Area(Place_Area, Game, card, who)
    else:
        print("%s的当前手牌："%P[who].name,end=' ')
        for i in P[who].card:
            print(i,end=' ')
        print()
        print("当前放置区的牌：",end=' ')
        for i in Place_Area.card:
            print(i, end=' ')
        #print("\nA:打出手牌\nB:摸牌")
        Operation = str(input('\n请输入要执行的操作:'))
        if Operation == 'B':
            card = P[who].Touch_Card(Cards)  # who摸牌
            print("卡组剩余：", Cards.sum)
            Put_Place_Area(Place_Area,Game,card,who)
        elif Operation == 'A':
            card = P[who].Knockout()         #P[who]打出
            Put_Place_Area(Place_Area,Game,card,who)
        elif Operation == 'S':
            break
    who = (who+1)%2
