# Author: Mr.Xu
# @Time : 2019/10/2 15:59
import os

view_meg = '''
请选择角色编号：
    1 管理员
    2 普通用户
    q 退出
'''
admin_msg = '''
    1.注册
    2.登陆
    3.上传视频
    4.删除视频
    5.发布公告
'''
user_msg = '''
    1.注册
    2.登陆
    3.冲会员
    4.查看视频
    5.下载免费电影
    6.下载收费视频
    7.查看观影记录
    8.查看公告
'''
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
UPLOAD_MOVIE_PATH = os.path.join(BASE_PATH, "upload_movies")

