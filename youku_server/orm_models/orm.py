# Author: Mr.Xu
# @Time : 2019/10/9 8:26
from orm_models import sql_control

class Filed:
    def __init__(self,name,type,primary_key,default):
        self.name = name
        self.type = type
        self.primary_key = primary_key
        self.default = default

class IntegerField(Filed):
    def __init__(self,name,type="int",primary_key=False,default=0):
        super().__init__(name,type,primary_key,default)

class StringField(Filed):
    def __init__(self,name,type="varchar(256)",primary_key=False,default=None):
        super().__init__(name,type,primary_key,default)

class Mymeta(type):
    def __new__(cls, class_name,base_class,class_attr):
        if class_name == "Models":
            return type.__new__(cls, class_name,base_class,class_attr)

        table_name = class_attr.get("table_name",class_name)
        primary_key = None
        mappings = {}
        for k,v in class_attr.items():
             if isinstance(v,Filed):
                 mappings[k]=v

                 if v.primary_key:
                    if primary_key:
                        raise Exception("只能有一个主键")

                    primary_key = v.name
        if not primary_key:
            raise Exception("必须有一个主键")

        for k in mappings.keys():
            class_attr.pop(k)

        class_attr["table_name"] = table_name
        class_attr["primary_key"] = primary_key
        class_attr["mappings"] = mappings
        return type.__new__(cls, class_name,base_class,class_attr)

class Models(dict,metaclass=Mymeta):
    sql_obj = sql_control.MySQL()

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def select_sql(cls,**kwargs):
        if not kwargs:
            # select * from XXX
            sql = f"select * from {cls.table_name}"
            res = cls.sql_obj.select(sql)
        else:
            key = list(kwargs.keys())[0]
            value = kwargs.get(key)
            # select * from xx where key = value
            sql = f"select * from {cls.table_name} where {key} = %s"
            res = cls.sql_obj.select(sql,value)
        return [cls(**i) for i in res]

    def instert_sql(self):
        values = []
        replace = []

        for k,v in self.mappings.items():
            values.append(
                getattr(self,v.name)
            )
            replace.append("?")

        # insert into xxx values(values)
        sql = f"insert into {self.table_name} values({','.join(replace)})"
        sql = sql.replace("?","%s")
        self.sql_obj.execute(sql,values)

    def update_sql(self):
        values=[]
        field=[]
        primary_key = None

        for k,v in self.mappings.items():
            if v.primary_key:
                primary_key = getattr(self,v.name)
            else:
                values.append(
                    getattr(self,v.name)
                )
                field.append(v.name+"=?")

        # update xxx set key=value where self.primary_key = primary_key
        sql = f"update {self.table_name} set {','.join(field)} where {self.primary_key} = {primary_key}"
        sql = sql.replace("?", "%s")
        self.sql_obj.execute(sql, values)
