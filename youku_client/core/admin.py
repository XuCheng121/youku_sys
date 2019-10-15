# Author: Mr.Xu
# @Time : 2019/10/9 9:06
from conf import settings
from lib import common
import os,time

user_info = {
    "cookies":None
}

def register(conn):
    user_name = input("请输入账号")
    pwd = input("请输入密码")
    re_pwd = input("请确认密码")

    if pwd != re_pwd:
        print("两次密码不一致")
        return

    send_dic = {
        "type":"register",
        "user_type":"admin",
        "user_name":user_name,
        "pwd":pwd,
    }
    back_dic = common.send_msg(send_dic,conn)
    print(back_dic.get("msg"))

def login(conn):
    user_name = input("请输入账号")
    pwd = input("请输入密码")

    send_dic = {
        "type": "login",
        "user_type": "admin",
        "user_name": user_name,
        "pwd": pwd,
    }
    back_dic = common.send_msg(send_dic, conn)
    if back_dic.get("flag"):
        user_info["cookies"] = back_dic.get("session")
    print(back_dic.get("msg"))

def upload_movie(conn):
    movie_list = os.listdir(settings.UPLOAD_MOVIE_PATH)
    if not movie_list:
        print("没有电影")
        return

    for index,movie in enumerate(movie_list):
        print(index,movie)

    choice = input("请输入电影编号")
    if choice.isdigit() and int(choice) in range(len(movie_list)):
        choice = int(choice)

        movie_name = movie_list[choice]
        movie_path = os.path.join(settings.UPLOAD_MOVIE_PATH,movie_name)
        movie_md5 = common.get_movie_md5(movie_path)
        movie_size = os.path.getsize(movie_path)
        send_dic = {
            "type": "check_movie",
            "session":user_info.get("cookies"),
            "movie_md5":movie_md5
        }
        back_dic = common.send_msg(send_dic, conn)
        print(back_dic.get("msg"))
        if back_dic.get("flag"):

            while 1:
                is_vip = input("是否免费1/0")
                if is_vip =="1"or is_vip=="0":
                    is_vip= int(is_vip)
                    break

            send_dic = {
                "type": "upload_movie",
                "session": user_info.get("cookies"),
                "movie_name": movie_name,
                "movie_md5": movie_md5,
                "movie_size" :movie_size,
                "is_vip":is_vip
            }
            back_dic = common.send_msg(send_dic, conn, movie_path)
            print(back_dic.get("msg"))
    else:
        print("输入错误")

def delete_movie(conn):
    send_dic = {
        "type": "get_movie_list",
        "session": user_info.get("cookies"),
        "is_free": 2
    }
    back_dic = common.send_msg(send_dic, conn)
    if back_dic.get("flag"):
        movie_list = back_dic.get("msg")
        for index, movie in enumerate(movie_list):
            print(index, movie)
        choice = input("请输入电影编号")
        if choice.isdigit() and int(choice) in range(len(movie_list)):
            choice = int(choice)
            movie_info = movie_list[choice]
            movie_id = movie_info[0]
            send_dic = {
                "type": "delete_movie",
                "session": user_info.get("cookies"),
                "movie_id":movie_id,
            }
            back_dic = common.send_msg(send_dic, conn)
            print(back_dic.get("msg"))
    else:
        print(back_dic.get("msg"))


def send_notice(conn):
    title = input("请输入公告标题")
    content = input("请输入公告内容")
    send_dic = {
        "type": "send_notice",
        "session": user_info.get("cookies"),
        "title": title,
        "content": content,
    }
    back_dic = common.send_msg(send_dic, conn)
    print(back_dic.get("msg"))


def view(conn):
    func_dic = {
        "1":register,
        "2":login,
        "3":upload_movie,
        "4":delete_movie,
        "5":send_notice,
    }
    while 1:
        print(settings.admin_msg)
        choice = input("请输入功能编号")
        if choice == "q":
            user_info["cookies"] = None
            break
        if choice in func_dic:
            func_dic[choice](conn)