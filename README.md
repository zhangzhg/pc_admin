# spider
查询并爬取笔趣阁小说，查看目录，加载章节并查看，支持浏览器和手机。django+scrapy+vue
## 安装PyCharm
## 创建工程目录
django-admin startproject pc_admin 
## 创建后端目录
cd pc_admin & python manage.py startapp backend 
## 创建前端目录
vue create frontend #vue-cli4 
`
// vue.config.js
module.exports = {
 // build 出來的結果會有個static目錄，backend就能訪問的到靜態文件
 assetsDir: 'static'
};
`
## 设置urls
`
urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', TemplateView.as_view(template_name="index.html")),
    path('api/', include('backend.urls'))
]
`
`
backend/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('search', views.search)
]
`
## 设置setting
`
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "frontend/dist"),
    os.path.join(BASE_DIR, "frontend/dist/static")
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['frontend/dist'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
`
## 编译前端
npm run build
## 启动后端
python manage.py runserver
## 生成迁移文件：根据模型类型生成sql语句
#生成sql
python manage.py makemigrations backend
## 执行sql 生成表，默认数据库sqllite
python manage.py migrate
python manager.py shell #数据库控制台
python manager.py createsuperuser #新建数据库管理用户
admin/admin 283605231@163.co
## 页面查看数据库：http://127.0.0.1:8000/admin/
## 中文支持 setting.py
LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

## model管理
#admin.py
from django.contrib import admin
from .models import *

## 如果需要通过/admin进行模型管理，需要进行注册
admin.site.register(BookIndex)


## **django整合scrapy,用于保存数据**
## 连接django与scrapy，其实就是用django的model直接保存文件，但是这个在scrapyd不能用。
pip install scrapy_djangoitem
`
#爬虫的setting.py
import os
import sys
sys.path.append('/../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'pc_admin.settings'

import django
django.setup()
`
#爬虫 items
`
from scrapy_djangoitem import DjangoItem
from backend import models


class BookItem(DjangoItem):
    django_model = models.BookItem

爬虫pipeline
class BookPipeline(object):
    def process_item(self, item, spider):
        item.save()
        return item
`
## 安装scrapyd 
pip install scrapyd
## 安装客户端scrapyd-client
pip3 install scrapyd-client
## 测试安装
scrapyd-deploy -h
如果上面的命令不可行，在path下新建：scrapyd-deploy.bat
"F:\soft\anaconda\python.exe" "F:\soft\anaconda\Scripts\scrapyd-deploy" %1 %2 %3 %4 %5 %6 %7 %8 %9

## 启动爬虫服务
scrapyd
#如果启动报错， 有可能包版本不对， 升级一下
pip install --upgrade attrs

## 发布爬虫
scrapyd-deploy 爬虫名称 -p 项目名称
1、获取状态
http://127.0.0.1:6800/daemonstatus.json
2、获取项目列表
http://127.0.0.1:6800/listprojects.json
3、获取项目下已发布的爬虫列表
http://127.0.0.1:6800/listspiders.json?project=myproject
4、获取项目下已发布的爬虫版本列表
http://127.0.0.1:6800/listversions.json?project=myproject
5、获取爬虫运行状态
http://127.0.0.1:6800/listjobs.json?project=myproject
 6、启动服务器上某一爬虫（必须是已发布到服务器的爬虫）
http://localhost:6800/schedule.json （post方式，data={"project":myproject,"spider":myspider}）
7、删除某一版本爬虫
http://127.0.0.1:6800/delversion.json （post方式，data={"project":myproject,"version":myversion}）
8、删除某一工程，包括该工程下的各版本爬虫
  
http://127.0.0.1:6800/delproject.json（post方式，data={"project":myproject}）

