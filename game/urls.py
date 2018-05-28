
from django.contrib import admin
from django.urls import path,re_path

from gameapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crawler/',views.crawler),
    path('',views.index),
    path('index/',views.index),
    path('login/',views.login),
    path('logout/',views.logout),
    path('register/',views.register),
    path('lovepage/',views.lovepage),
    re_path('detail/(\d+)/$',views.detail),
    re_path('adtlovelist/(\w+)/(\d+)/$',views.adtlovelist)
]
