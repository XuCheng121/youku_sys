# Author: Mr.Xu
# @Time : 2019/10/9 10:01
from db import models,user_data
import datetime,os
from lib import common
from conf import settings

@common.login_auth
def upload_movie_interface(user_dic,conn):
    movie_name = user_dic.get("movie_name")
    movie_path = os.path.join(settings.DOWNLOAD_MOVIES_PATH,movie_name)
    movie_size = user_dic.get("movie_size")
    recv_len = 0
    with open(movie_path,"wb")as f:
        while recv_len<movie_size:
            recv_data = conn.recv(1024)
            f.write(recv_data)
            recv_len += len(recv_data)

    movie_obj = models.Movie(
        movie_name = movie_name,
        is_free=user_dic.get("is_vip"),
        is_delete = 0,
        file_md5 = user_dic.get("movie_md5"),
        path = movie_path,
        upload_time = datetime.datetime.now(),
        user_id = user_dic.get("user_id"),
    )
    movie_obj.instert_sql()

    send_dic = {
        "flag": True,
        "msg": "上传成功",
    }
    common.send_msg(send_dic, conn)


@common.login_auth
def delete_movie_interface(user_dic,conn):
    movie_obj = models.Movie.select_sql(movie_id=user_dic.get("movie_id"))[0]
    movie_obj.is_delete = 1
    movie_obj.update_sql()
    send_dic = {
        "flag": True,
        "msg": "删除成功",
    }
    common.send_msg(send_dic, conn)

@common.login_auth
def send_notice_interface(user_dic,conn):
    notice_obj = models.Notice(
        title = user_dic.get("title"),
        content = user_dic.get("content"),
        create_time = datetime.datetime.now(),
        user_id = user_dic.get("user_id"),
    )
    notice_obj.instert_sql()
    send_dic = {
        "flag": True,
        "msg": "发布成功",
    }
    common.send_msg(send_dic, conn)
