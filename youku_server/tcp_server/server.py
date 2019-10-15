
import socket
from concurrent.futures import ThreadPoolExecutor
from interface import common_interface,admin_interface,user_interface
from lib import common
from db import user_data

pool = ThreadPoolExecutor(100)

func_dic = {
    "register" : common_interface.register_interface,
    "login" : common_interface.login_interface,
    "check_movie" : common_interface.check_movie_interface,
    "upload_movie" : admin_interface.upload_movie_interface,
    "get_movie_list" : common_interface.get_movie_list_interface,
    "delete_movie" : admin_interface.delete_movie_interface,
    "send_notice" : admin_interface.send_notice_interface,
    "pay_vip" : user_interface.pay_vip_interface,
    "download_movie" : user_interface.download_movie_interface,
    "show_movie_record" : user_interface.show_movie_record_interface,
    "show_notice" : user_interface.show_notice_interface,
}

def run():
    server = socket.socket()
    server.bind(("127.0.0.1",8080))
    server.listen(5)
    while 1:
        conn,addr = server.accept()
        pool.submit(task_socket,conn,addr)

def task_socket(conn,addr):
    while 1:
        try:
            user_dic = common.recv_msg(conn)

            func_type = user_dic.get("type")
            if func_type not in func_dic:
                send_dic = {
                    "flag":False,
                    "msg": "功能错误",
                }
                common.send_msg(send_dic,conn)
                continue

            user_dic["addr"] = addr
            print("进入",func_type)
            func_dic[func_type](user_dic,conn)
        except Exception as e:
            print(e)
            user_data.mutex.acquire()
            user_data.online_user.pop(addr)
            user_data.mutex.release()
            break

