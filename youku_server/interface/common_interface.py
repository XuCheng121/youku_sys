# Author: Mr.Xu
# @Time : 2019/10/9 9:16
from db import models,user_data
import datetime
from lib import common


def register_interface(user_dic,conn):
    user_list = models.User.select_sql(user_name = user_dic.get("user_name"))
    pwd = user_dic.get("pwd")
    if not user_list:
        user_obj = models.User(
            user_name = user_dic.get("user_name"),
            pwd = common.get_pwd_md5(pwd),
            register_time = datetime.datetime.now(),
            is_vip=0,
            is_locked = 0,
            user_type = user_dic.get("user_type"),
        )
        user_obj.instert_sql()
        send_dic = {
            "flag": True,
            "msg": "注册成功",
        }
        common.send_msg(send_dic, conn)
    else:
        send_dic = {
            "flag": False,
            "msg": "注册失败",
        }
        common.send_msg(send_dic, conn)


def login_interface(user_dic,conn):
    user_list = models.User.select_sql(user_name=user_dic.get("user_name"))
    if user_list:
        user_obj = user_list[0]
        user_name = user_obj.get("user_name")
        pwd = user_dic.get("pwd")
        if user_obj.pwd == common.get_pwd_md5(pwd):

            session = common.get_session(user_name)
            addr = user_dic.get("addr")
            user_data.mutex.acquire()
            user_data.online_user[addr] = [session,user_obj.user_id]
            user_data.mutex.release()
            print(user_data.online_user)
            send_dic = {
                "flag": True,
                "msg": "登陆成功",
                "session":session,
                "is_vip":user_obj.is_vip
            }
            common.send_msg(send_dic, conn)
        else:
            send_dic = {
                "flag": False,
                "msg": "登陆失败",
            }
            common.send_msg(send_dic, conn)
    else:
        send_dic = {
            "flag": False,
            "msg": "登陆失败",
        }
        common.send_msg(send_dic, conn)


@common.login_auth
def check_movie_interface(user_dic,conn):
    movie_list = models.Movie.select_sql(file_md5=user_dic.get("movie_md5"))
    if not movie_list:
        send_dic = {
            "flag": True,
            "msg": "可以上传",
        }
        common.send_msg(send_dic, conn)
    else:
        send_dic = {
            "flag": False,
            "msg": "电影已经存在",
        }
        common.send_msg(send_dic, conn)


@common.login_auth
def get_movie_list_interface(user_dic,conn):
    movie_list = models.Movie.select_sql(is_delete=0)
    if movie_list:
        movie_info = []
        for obj in movie_list:
            if obj.is_free == user_dic.get("is_free") or user_dic.get("is_free")==2:
                movie_info.append(
                    [obj.movie_id,
                     obj.movie_name,
                     "免费" if obj.is_free else "收费"]
                )
        if movie_info:
            send_dic = {
                "flag": True,
                "msg": movie_info
            }
            common.send_msg(send_dic, conn)
        else:
            send_dic = {
                "flag": False,
                "msg": "没有电影",
            }
            common.send_msg(send_dic, conn)

    else:
        send_dic = {
            "flag": False,
            "msg": "没有电影",
        }
        common.send_msg(send_dic, conn)