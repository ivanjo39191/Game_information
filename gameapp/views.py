from django.shortcuts import render,redirect,render_to_response
from gameapp.models import gamee,User
from . import models
from django.http import HttpResponse
from django import forms
from gameapp.forms import UserForm,RegisterForm
import hashlib #密碼加密
import html #html轉譯
from django.core.paginator import Paginator


import requests
from bs4 import BeautifulSoup
import urllib
import re
global titles,links,at,ct,t,l,timg1

#主圖片爬蟲
def titleimg():
    global timg1
    url = 'https://forum.gamer.com.tw/A.php?bsn=31406'   #選擇網址
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15' #偽裝使用者
    headers = {'User-Agent':user_agent}
    data_res = urllib.request.Request(url=url,headers=headers)
    data = urllib.request.urlopen(data_res)
    data = data.read().decode('utf-8')  
    sp = BeautifulSoup(data, "html.parser")

    titleimg = sp.find("div",{"class":"FM-abox1"}).findAll("img", src = re.compile('/welcome/'))

    for timg in titleimg:
        timg1 = timg['src']

titleimg() #運行主圖片爬蟲





def hash_code(s, salt='ivan'): #密碼加密
    h = hashlib.sha256()
    s = s + salt
    h.update(s.encode())
    return h.hexdigest()

def index(request):

    timg2 = timg1 #將主圖片爬蟲轉為區域變數才能傳遞
    unit = gamee.objects.all().order_by( '-id' ) 
    paginator = Paginator(unit, 5) #每5篇進行分頁
    page_num = request.GET.get('page', 1) #獲取url的頁面參數 (GET請求)
    page_of_units = paginator.get_page(page_num) #get_page會自動識別頁碼，若無效則返回1，超出頁數則顯示最後一頁
    context = {}
    context['units'] = page_of_units.object_list
    context['page_of_units'] = page_of_units
    return render(request,"index.html",context)



def login(request):
    timg2 = timg1
    if request.session.get('is_login',None): #檢查session確定是否登入，不允許重複登入
        return redirect("/index/")  #若已登入則導向主頁
    if request.method == 'POST':    #接收POST訊息，若無則讓返回空表單
        login_form = UserForm(request.POST)   #導入表單模型
        if login_form.is_valid(): #驗證表單
            username = login_form.cleaned_data['username']  #從表單的cleaned_data中獲得具體值
            password = login_form.cleaned_data['password'] 
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password): #密文處理
                    #使用session寫入登入者資料
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['user_love'] = user.clove
                    message = "登入成功"
                    return redirect('/index/')
                else:
                    message = "密碼不正確"
            except:
                message = "該用戶不存在"
    login_form = UserForm(request.POST) #返回空表單
    return render(request,"login.html",locals())

def logout(request):
    if not request.session.get('is_login',None): #如果原本未登入，就不需要登出
        return redirect('/index/')
    request.session.flush() #一次性將session內容全部清除
    return redirect('/index/')

def register(request):
    timg2 = timg1
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = '請檢察填寫的內容!'
        if register_form.is_valid(): #驗證數據，提取表單內容
            username = register_form.cleaned_data['username'] 
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2: #若兩次密碼不同
                message = "兩次輸入的密碼不同!"
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username) #比對資料庫是否有相同用戶名
                if same_name_user:
                    message = "該用戶名稱已存在!"
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)  #比對資料庫是否有相同信箱
                if same_email_user:
                    message = "信箱已被使用!"
                    return render(request, 'register.html', locals())
                #若上面條件皆通過，則創建新的用戶
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/') #自動跳轉到登入頁面
    register_form = RegisterForm(request.POST)
    return render(request, 'register.html', locals())

def detail(request, detailid=None):
    timg2 = timg1
    unit = gamee.objects.get(id=detailid)
    cTitle = unit.cTitle
    cAuthor = unit.cAuthor
    cContent = html.unescape(unit.cContent).replace("data-src","src") 

    #cContent反轉譯，且由於巴哈有延遲載入，因此src屬性名稱不同需替換
    return render(request,"detail.html",locals())

def crawler(request):  #爬蟲程式
    global titles,links,at,ct,t,l
    url = 'https://forum.gamer.com.tw/B.php?bsn=31406'   #選擇網址
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15' #偽裝使用者
    headers = {'User-Agent':user_agent}
    data_res = urllib.request.Request(url=url,headers=headers)
    data = urllib.request.urlopen(data_res)
    data = data.read().decode('utf-8')  
    sp = BeautifulSoup(data, "html.parser")


    title = sp.findAll('td',{"class":"b-list__main"})
    titles = []
    for titlee in title:
        titles.append(titlee.text.strip('\n'))

    links = []
    ll = 'https://forum.gamer.com.tw/'
    link = sp.find("table",{"class":"b-list"}).findAll("a", href = re.compile('C.php?'))
    for linkk in link:
        page = re.compile(r'^((?!page).)*$')  ##不匹配page
        last = re.compile(r'^((?!last).)*$')  ##不匹配last
        m = page.match(linkk['href'])  ##設定變數m來排除page
        if m != None:  ##若不為None (None會跳出例外)
            n = last.match(m.group(0)) ## 設定變數n來排除last
            if n != None: ##若不為None (None會跳出例外)
                links.append(ll+n.group(0))

    for t,l in zip(titles,links):
        print(t,l)
        content(l) #使用爬蟲出來的網址進行文章內容的爬蟲
        sql()  #將爬出的內容進行與資料庫的連接
    return redirect('/index/')

def titleimg(request):
    global timg1
    url = 'https://forum.gamer.com.tw/A.php?bsn=31406'   #選擇網址
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15' #偽裝使用者
    headers = {'User-Agent':user_agent}
    data_res = urllib.request.Request(url=url,headers=headers)
    data = urllib.request.urlopen(data_res)
    data = data.read().decode('utf-8')  
    sp = BeautifulSoup(data, "html.parser")

    titleimg = sp.find("div",{"class":"FM-abox1"}).findAll("img", src = re.compile('/welcome/'))

    for timg in titleimg:
        timg1 = timg['src']
    print(timg1)


def content(aa):
    global titles,links,at,ct,t,l
    url = aa   #選擇網址
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15' #偽裝使用者
    headers = {'User-Agent':user_agent}
    data_res = urllib.request.Request(url=url,headers=headers)
    data = urllib.request.urlopen(data_res)
    data = data.read().decode('utf-8')  
    sp = BeautifulSoup(data, "html.parser")

    authors = sp.find('div',{"class":"c-post__header__author"}).findAll("a",{"class":"username"})
    for author in authors:
        at = author.text
        print(at)

    contents = sp.find('div',{"class":"c-article__content"})
    ct = html.escape(str(contents))#html編碼轉譯
    print(ct)

def sql():
    global titles,links,at,ct,t,l

    cAuthor = at    
    cContent = ct
    cTitle = t
    cLink = l
    try:
        if gamee.objects.get(cTitle=t):
            print('已有重複資料')
            
    except:
        unit = gamee.objects.create(cAuthor=cAuthor, cContent=cContent, cTitle=cTitle, cLink=cLink) 
        unit.save()                      #寫入資料庫
        print('成功儲存一筆資料')
        


#我的最愛列表
def lovepage(request):
    timg2 = timg1
    ut = models.User.objects.get(id=request.session['user_id']) #提取使用者資料表
    #將會在前台使用 ut.clove 我的最愛串列

    return render(request,"lovepage.html",locals())

#加入、刪除我的最愛文章
def adtlovelist (request, ctype=None, loveid = None): # ctype決定加入或是刪除,loveid則是傳入的文章id
    userinfo = models.User.objects.get(id=request.session['user_id']) #讀取使用者id
    lovelist = userinfo.clove #將我的最愛列表暫時存入lovelist串列
    redetail = '/detail/' + loveid #取得當前詳細頁網址
    if ctype == 'add': #加入最愛文章
        love = gamee.objects.get(id=loveid) #讀取遊戲資訊列表
        flag = True #設定檢查旗標
        for unit in userinfo.clove: #檢查是否已有相同標題
            if love.cTitle == unit[1]: #如果遊戲資訊標題==使用者我的最愛標題 就不存入
                flag = False
                break
        if flag: #如果文章不存在
            temlist = [] #暫時串列
            temlist.append(love.cAuthor)
            temlist.append(love.cTitle)
            temlist.append(love.cLink)
            temlist.append(love.id)
            lovelist.append(temlist) #將暫時串列加入我的最愛串列

            userinfo.clove = lovelist #將我的最愛串列寫入資料庫
            userinfo.save() #儲存資料庫
            
        return redirect(redetail) #跳轉回詳細頁面網址

    elif ctype == 'delete':  #刪除我的最愛文章
        del lovelist[int(loveid)] #從我的最愛中移除該文章，用計數器的方式取得list的項數
        userinfo.clove = lovelist #將刪除後的我的最愛串列寫入資料庫
        userinfo.save() #儲存資料庫

        return redirect('/lovepage/') #跳轉到我的最愛列表頁面


