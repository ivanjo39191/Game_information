from django.db import models
import ast
 #自定義field

class ListField(models.TextField):

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

#遊戲資訊資料表
class gamee(models.Model):
    cAuthor = models.TextField(max_length=255, blank=True) #建立字串型別的欄位，最大長度為20字元，欄位不可空白
    cContent = models.TextField(max_length=99999,blank=True, default='')
    cTitle = models.CharField(max_length=100,blank=True, default='')#blank=True 欄位可空白
    cLink = models.CharField(max_length=100,blank=True, default='')

 
    def __str__(self):
        return self.cTitle #表示顯示cTitle欄位

class User(models.Model):
    gender = (
        ('male','男'),
        ('female','女'),
    )
    name = models.CharField(max_length=128, unique = True) #唯一，不可有相同姓名
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default="男")
    ctime = models.DateTimeField(auto_now_add=True)
    clove = ListField(blank=True)

    def __str__(self):
        return self.name

class lovemode(models.Model):
    cAuthor = models.TextField(max_length=255, blank=True) #建立字串型別的欄位，最大長度為20字元，欄位不可空白
    cContent = models.TextField(max_length=99999,blank=True, default='')
    cTitle = models.CharField(max_length=100,blank=True, default='')#blank=True 欄位可空白
    cLink = models.CharField(max_length=100,blank=True, default='')
    def __str__(self):
        return self.cTitle #表示顯示cTitle欄位