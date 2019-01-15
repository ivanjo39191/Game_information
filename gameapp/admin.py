from django.contrib import admin

from gameapp.models import gamee
from gameapp.models import User
 
#下面會以register的方式，將建立的資料模型向admin註冊
class gameAdmin(admin.ModelAdmin):
    list_display=('id','cTitle','cAuthor','cContent','cLink')
admin.site.register(gamee,gameAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display=('id','name','password','email','sex','ctime','clove')
admin.site.register(User,UserAdmin)
