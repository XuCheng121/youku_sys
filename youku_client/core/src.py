# Author: Mr.Xu
# @Time : 2019/10/9 9:02
from conf import settings
from tcp_client import client
from core import admin,user

def run():
    func_dic = {
        "1":admin.view,
        "2":user.view,
    }
    conn = client.get_client()
    while 1:
        print(settings.view_meg)
        choice = input("请输入功能编号")
        if choice == "q":
            break
        if choice in func_dic:
            func_dic[choice](conn)