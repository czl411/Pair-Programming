#coding = utf-8
import requests
def GET_Token_And_C_Header(URL):         #获取token并返回header
    id = input("请输入学号：")
    password = input("请输入密码：")
    url = URL
    data={
        "student_id": id,
        "password": password
    }
    res = requests.post(url,data).json()
    token = res["data"]["token"]
    token = "Bearer "+token
    header={
        "Authorization": token
    }
    print("登录成功！")
    return header

def C_Game(URL,header,attribute):       #创建房间，并返回uuid
    pro_res = requests.post(URL, headers=header,data=attribute).json()
    print("创建对局成功！")
    return pro_res["data"]["uuid"]

def Join_Game(URL,uuid,header):         #加入房间
    URL=URL+"/"+uuid
    print("加入对局成功")
    return requests.post(URL, headers=header).json()

def Player_operation(URL,uuid,header,operation):    #玩家操作
    URL=URL+"/"+uuid
    print("玩家操作成功！")
    return requests.put(URL, data=operation, headers=header).json()

def Get_Previous_operation(URL,uuid,header):             #返回上步操作
    URL=URL+"/"+uuid+"/last"
    print("获取上步操作成功！")
    return requests.get(URL,headers=header).json()

def Get_Match_info(URL,uuid,header):                     #获取对局信息
    URL=URL+"/"+uuid
    print("获取对局信息成功！")
    return requests.get(URL,headers=header).json()

def Get_Match_list(URL,header,data):                #获取对局列表
    URL=URL+"/index"
    print("获取对局列表成功！")
    return requests.get(URL,params=data, headers=header).json()

# '''
# 登录接口
# '''
# url1="http://172.17.173.97:8080/api/user/login"
# header = GET_Token_And_C_Header(url1)
# print(header["Authorization"])
# '''
# 创建对局
# '''
# url2="http://172.17.173.97:9000/api/game"
# attribute={
#     "pravite":False
# }
# uuid=C_Game(url2,header,attribute)
# print(uuid)
# print(Join_Game(url2,uuid,header))
# '''
# 获取上步操作
# '''
# res3=Get_Previous_operation(url2,uuid,header)
# print(res3)
# print(len(res3["data"]["last_code"]))
# '''
# 执行玩家操作
# '''
# operation1={
#     #摸牌
#     "type":0
# }
# operation2={
#     #出牌
#     "type":1,
#     "card":"SQ"
# }
#
# res2=Player_operation(url2,uuid,header,operation1)
# print(res2)
#
# '''
# 获取对局信息
# '''
# res4=Get_Match_info(url2,uuid,header)
# print(res4)
# '''
# 获取对局列表
# '''
# data_ye={
#     "page_size":3,
#     "page_num":2
#
# }
# res4=Get_Match_list(url2,header,data_ye)
# print(res4)



