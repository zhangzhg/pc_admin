from django.contrib import admin
from .models import *


# 如果需要通过/admin进行管理，需要进行注册
admin.site.register(BookIndex)
admin.site.register(BookItem)
admin.site.register(BookChapter)