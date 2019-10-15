# Author: Mr.Xu
# @Time : 2019/10/9 9:17
import json,struct,hashlib,uuid
from db import user_data

def recv_msg(conn):
    head = conn.recv(4)
    data_len = struct.unpack("i", head)[0]
    recv_data = conn.recv(data_len)
    back_dic = json.loads(recv_data)
    return back_dic

def send_msg(send_dic,conn,file=None):
    json_data = json.dumps(send_dic).encode("utf8")
    head = struct.pack("i", len(json_data))
    conn.send(head)
    conn.send(json_data)
    if file:
        with open(file,"rb") as f:
            for line in f:
                conn.send(line)

def get_pwd_md5(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode("utf8"))
    md5.update("xc".encode("utf8"))
    return md5.hexdigest()

def get_session(user_name):
    md5 = hashlib.md5()
    md5.update(user_name.encode("utf8"))
    md5.update(str(uuid.uuid4()).encode("utf8"))
    return md5.hexdigest()

def login_auth(func):
    def inner(*args,**kwargs):
        user_dic = args[0]
        user_session = user_dic.get("session")
        addr = user_dic.get("addr")
        server_session = user_data.online_user.get(addr)
        print(user_session,server_session)
        if server_session and user_session == server_session[0]:
            args[0]["user_id"] = server_session[1]
            res = func(*args,**kwargs)
            return res
        else:
            send_dic = {
                "flag": False,
                "msg": "请先登陆",
            }
            send_msg(send_dic, args[1])
    return inner
