# Author: Mr.Xu
# @Time : 2019/10/5 16:47
from orm_models.orm import Models,IntegerField,StringField

'''
- 用户表: User
        - id
        - name
        - pwd
        - register_time 注册时间
        - is_vip 是否是VIP  0/1
        - is_locked 是否被锁定 0/1
        - user_type 管理员用户/普通用户

    - 电影表  Movie
        - id
        - m_name
        - is_free  免费/收费 0/1
        - is_delete  电影是否被删除
        - file_md5  校验电影文件的唯一性
        - path  电影的存放目录
        - upload_time  电影上传时间
        - user_id

    - 公告表  Notice
        - id
        - title
        - content
        - create_time
        - user_id

    - 下载记录表 DownloadRecord
        - id
        - user_id
        - movie_id
        - download_time
'''

class User(Models):
    table_name = "user"
    user_id = IntegerField(name="user_id",primary_key=True)
    user_name = StringField(name="user_name")
    pwd = StringField(name="pwd")
    register_time = StringField(name="register_time")
    is_vip = IntegerField(name="is_vip")
    is_locked = IntegerField(name="is_locked")
    user_type = StringField(name="user_type")

class Movie(Models):
    table_name = "movie"
    movie_id = IntegerField(name="movie_id", primary_key=True)
    movie_name = StringField(name="movie_name")
    is_free = IntegerField(name="is_free")
    is_delete = IntegerField(name="is_delete")
    file_md5 = StringField(name="file_md5")
    path = StringField(name="path")
    upload_time = StringField(name="upload_time")
    user_id = IntegerField(name="user_id")

class Notice(Models):
    table_name = "notice"
    n_id = IntegerField(name="n_id", primary_key=True)
    title = StringField(name="title")
    content = StringField(name="content")
    create_time = StringField(name="create_time")
    user_id = IntegerField(name="user_id")

class DownloadRecord(Models):
    table_name = "download_record"
    download_id = IntegerField(name="download_id", primary_key=True)
    user_id = IntegerField(name="user_id")
    movie_id = IntegerField(name="movie_id")
    download_time = StringField(name='download_time')

if __name__ == '__main__':
    user_obj = User.select_sql(user_name='xc')[0]
    print(user_obj)  # [{}] h --> [obj]
    # user_obj.user_name = "11"
