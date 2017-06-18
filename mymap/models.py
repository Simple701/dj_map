from django.db import models

# Create your models here.
class Post(models.Model):
    author = models.CharField(u'用户',max_length=50)
    mk_id = models.CharField(u'ID',max_length=120)
    title = models.CharField(u'标题',max_length=100)
    time = models.DateTimeField(u'更新时间',auto_now=True, null=True)
    content = models.TextField(u'内容')
    def __str__ (self):
        return str(self.id)

class Marker(models.Model):
    pointx = models.CharField(u'X',max_length=50)
    pointy = models.CharField(u'Y',max_length=50)
    mdate = models.CharField(u'日期',max_length=50)
    title = models.CharField(u'标题',max_length=100)
    author = models.CharField(u'用户',max_length=30)
    time = models.DateTimeField(u'更新时间',auto_now=True, null=True)
    img = models.CharField(u'主图',max_length=120)
    def __str__ (self):
        return str(self.id)
