# Author: Mr.Xu
# @Time : 2019/10/9 9:11
import json,struct,hashlib,os

def send_msg(send_dic,conn,file=None):
    json_data = json.dumps(send_dic).encode("utf8")
    head = struct.pack("i",len(json_data))
    conn.send(head)
    conn.send(json_data)

    if file:
        with open(file,"rb") as f:
            for line in f:
                conn.send(line)

    head = conn.recv(4)
    data_len = struct.unpack("i",head)[0]
    recv_data = conn.recv(data_len)
    back_dic = json.loads(recv_data)
    return back_dic

def get_movie_md5(path):
    md5 = hashlib.md5()
    movie_size = os.path.getsize(path)
    with open(path,"rb") as f:
        for i in range(0,movie_size,movie_size//5):
            f.seek(i)
            md5.update(f.read(20))
    return md5.hexdigest()
