from online import *
import Game_online
import time
import keyboard

def kk(url,uuid,header,operation,Player,Cards,Place_Area):
    res = Player_operation(url, uuid, header, operation)  # 执行操作，并返回用来更新本地数据
    card = res["data"]["last_code"][4:]
    #if card not in Place_Area.card:     # 判断是否在放置区
    Place_Area.Put_in(card)         # 放进放置区
    Cards.Updata_Card_zu(card)          # 更新卡组
    if Place_Area.Whether_Eat_Cards():
        Player.Eat_Cards(Place_Area)

def Auto_Play(url,uuid,header,operation,Player,Cards,Place_Area):
    if Player.sum != 0:
        if Place_Area.sum != 0:
            for card in Player.card:
                if card[0] != Place_Area.card[Place_Area.sum-1][0]:
                    operation["type"] = 1
                    operation["card"] = card
                    Player.card.pop(Player.card.index(card))        #pop出
                    Player.sum -= 1
                    kk(url, uuid, header, operation, Player, Cards, Place_Area)
                    return
        else:
            operation["type"] = 1
            operation["card"] = Player.card[0]
            Player.card.pop(0)
            Player.sum -= 1
            kk(url, uuid, header, operation, Player, Cards, Place_Area)
            return

    kk(url,uuid,header,operation,Player,Cards,Place_Area)
    return

def Print_info(Cards,Place_Area,OWN,OPPONENT):
    print("以下分别为卡组、放置区、本地、对手的卡牌信息")
    print("卡组：",Cards.sum, ' ', Cards.card)
    print("放置：",Place_Area.sum, ' ', Place_Area.card)
    print("自己：",OWN.sum, ' ', OWN.card)
    print("对手：",OPPONENT.sum, ' ', OPPONENT.card)

Cards = Game_online.Card_zu()
P = []
P.append(Game_online.Player("陈志良"))
P.append(Game_online.Player("李知恩"))
Place_Area = Game_online.Placement_Area()

url1 = "http://172.17.173.97:8080/api/user/login"  # 登录接口
url2 = "http://172.17.173.97:9000/api/game"  # 创建游戏接口
header = GET_Token_And_C_Header(url1)
attribute = {
    "pravite": False
}
self_id = int()
uuid = str()
f1 = input("创建对局输入：1\n加入对局输入：2\n")
if f1 == '1':
    self_id = 0
    shuxing = input("创建私人房间输入：c\n创建公开房间输入：o\n")
    if shuxing == 'c':
        attribute["pravite"] = True
    uuid = C_Game(url2, header, attribute)
    print(uuid)
elif f1 == '2':
    self_id = 1
    uuid = input("请输入要加入的房间号：")
    Join_Game(url2, uuid, header)

while 1:                        #判断是否可以开始游戏，每2秒请求一次
    res = Get_Previous_operation(url2, uuid, header)
    if res["code"] == 200:
        print("游戏开始！")
        State_zh = res["data"]["your_turn"]
        TG_F = -1
        break
    else:
        time.sleep(2)

while 1:
    type = 0
    res = Get_Previous_operation(url2, uuid, header)    #获取上步操作
    if res["code"] != 200:                              #游戏结束，跳出
        break

    Last_operation = res["data"]["last_code"]           #存上步操作数据
    Your_Turn = res["data"]["your_turn"]
    if State_zh != Your_Turn:
        print(res["data"]["last_msg"])
        State_zh = Your_Turn
        if len(Last_operation) > 0:
            OP_type = Last_operation[2]             #操作类型：0=翻牌，1=打出手牌
            card = Last_operation[4:]               #什么牌
            if Your_Turn:                           #对面玩家打出手牌，更新本地对面玩家手牌数据
                Cards.Updata_Card_zu(card)          # 卡组更新
                Place_Area.Update(card)             # 放置堆更新
                if OP_type == '1':
                    P[1-self_id].Update_Player_Card(card)
                if Place_Area.Whether_Eat_Cards():                      #判定对面玩家是否吃牌
                    P[1-self_id].Eat_Cards(Place_Area)             #本地执行对面玩家吃牌，更新本地对面玩家手牌数据
        Print_info(Cards, Place_Area, P[self_id], P[1 - self_id])

    if keyboard.is_pressed('ctrl'):
        TG_F *= -1
        if TG_F == 1:
            print("开启托管")
        if TG_F == -1:
            print("关闭托管")

    if Your_Turn == True:
        operation = {
            "type": 0
        }
        if TG_F == 1:
            Auto_Play(url2,uuid,header,operation,P[self_id],Cards,Place_Area)
            continue
        if P[self_id].sum == 0:           #没手牌，默认摸牌
            kk(url2, uuid, header, operation, P[self_id], Cards, Place_Area)
            continue
        else:
            type = int(input("请输入要执行的操作：（0摸牌，1打出手牌）\n"))

            if type == 1:
                card = P[self_id].Knockout()
                operation["type"] = type
                print(card)
                operation["card"] = card
            kk(url2, uuid, header, operation, P[self_id], Cards, Place_Area)

res_end = Get_Match_info(url2,uuid,header)
print(res_end["data"]["host_hand"])
print(res_end["data"]["client_hand"])
if res_end["data"]["winner"] == self_id:
    print("YOU WIN!")
else:
    print("YOU LOSE!")
