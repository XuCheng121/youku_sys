# Author: Mr.Xu
# @Time : 2019/10/9 10:39
from db import models,user_data
import datetime,os
from lib import common
from conf import settings

@common.login_auth
def pay_vip_interface(user_dic,conn):
    user_obj = models.User.select_sql(user_id=user_dic.get("user_id"))[0]
    user_obj.is_vip = 1
    user_obj.update_sql()
    send_dic = {
        "flag": True,
        "msg": "会员充值成功",
    }
    common.send_msg(send_dic, conn)

@common.login_auth
def download_movie_interface(user_dic,conn):
    movie_obj = models.Movie.select_sql(movie_id=user_dic.get("movie_id"))[0]
    movie_path = movie_obj.path
    send_dic = {
        "movie_name": movie_obj.movie_name,
        "movie_size": os.path.getsize(movie_path)
    }
    common.send_msg(send_dic, conn, movie_path)

    download_obj = models.DownloadRecord(
        user_id = user_dic.get("user_id"),
        movie_id = user_dic.get("movie_id"),
        download_time = datetime.datetime.now()
    )
    download_obj.instert_sql()


@common.login_auth
def show_movie_record_interface(user_dic,conn):
    movie_list = models.DownloadRecord.select_sql(user_id=user_dic.get("user_id"))
    if movie_list:
        movie_info = []
        for obj in movie_list:
            movie_obj = models.Movie.select_sql(movie_id=obj.movie_id)[0]
            movie_info.append(
                [movie_obj.movie_name, str(obj.download_time)]
            )
        send_dic = {
            "flag": True,
            "msg": movie_info,
        }
        common.send_msg(send_dic, conn)
    else:
        send_dic = {
            "flag": False,
            "msg": "没有记录",
        }
        common.send_msg(send_dic, conn)

@common.login_auth
def show_notice_interface(user_dic,conn):
    notice_list = models.Notice.select_sql()
    if notice_list:
        notice_info = []
        for obj in notice_list:
            notice_info.append(
                [obj.title, obj.content]
            )
        send_dic = {
            "flag": True,
            "msg": notice_info,
        }
        common.send_msg(send_dic, conn)
    else:
        send_dic = {
            "flag": False,
            "msg": "没有公告",
        }
        common.send_msg(send_dic, conn)

