import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

"""
为投票应用定义模型，也就是数据库结构设计和附加的其它元数据

每个模型被表示为 django.db.models.Model 类的子类

每个字段都是 Field 类的实例，比如，字符字段被表示为 CharField ，日期时间字段被表示为 DateTimeField 

每个 Field 类实例变量的名字（例如 question_text 或 pub_date ）也是字段名，数据库会将它们作为列名

定义某些 Field 类实例需要参数，例如 CharField 需要一个 max_length 参数

可以使用 ForeignKey 定义了关系，比如下面的代码，每个 Choice 对象都关联到一个 Question 对象

Django 支持所有常用的数据库关系：多对一、多对多和一对一

另外请注意以下关于命名的几点：
数据库的表名是由应用名(polls)和模型名的小写形式(question和choice)连接而来
主键(IDs)会被自动创建，Django 会在外键字段名后追加字符串"_id"，外键关系由 FOREIGN KEY 生成
"""

# # Question 问题模型包括问题描述和发布时间
# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('发布时间')
#
#
# # Choice 选项模型也有两个字段，选项描述和当前得票数，每个选项属于一个问题
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

# 完成上述代码后还需要激活模型，或者说改变模型的三部曲：
# 编辑 models.py 文件，首次编辑时注意注册应用，或者说是在 settings.py 的 INSTALLED_APPS 中安装应用，
# 然后运行 makemigrations 命令为模型的改变生成迁移文件，
# 最后使用 migrate 命令应用数据库迁移


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # 给Question增加__str__()方法
    def __str__(self):
        return self.question_text

    # # 当 pub_date 为未来某天时，
    # # Question.was_published_recently() 应该返回 False
    # def was_published_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.pub_date <= now
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


# Choice模型有两个字段，选项描述和当前得票数
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # 给模型增加__str__()方法是很重要的，这不仅仅能给你在命令行里使用带来方便，Django自动生成的admin里也使用这个方法来表示对象
    def __str__(self):
        return self.choice_text
