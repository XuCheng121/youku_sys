# Author: Mr.Xu
# @Time : 2019/10/9 9:04
import socket

client = socket.socket()
client.connect(("127.0.0.1",8080))

def get_client():
    return client