from django.db import models

# Create your models here.

class Userinfo(models.Model):
    '''
    员工表
    '''
    name = models.CharField(max_length=32,verbose_name='姓名')   #姓名
    pwd = models.CharField(max_length=32,verbose_name='密码')    #密码

    class Meta:
        verbose_name_plural= '员工表'
    def __str__(self):
        return self.name

class ClassList(models.Model):
    '''
    班级表
    '''
    title = models.CharField(max_length=32,verbose_name='班级名')     #班级称号

    class Meta:
        verbose_name_plural= '班级表'
    def __str__(self):
        return self.title

class Student(models.Model):
    '''
    学生表
    '''
    user = models.CharField(max_length=32,verbose_name='姓名')      #姓名
    pwd = models.CharField(max_length=32,verbose_name='密码')       #密码
    cls = models.ForeignKey(to=ClassList,verbose_name='班级')       #班级id

    class Meta:
        verbose_name_plural= '学生表'
    def __str__(self):
        return self.user

class Questionnaire(models.Model):
    '''
    问卷表
    '''
    title = models.CharField(max_length=64,verbose_name='标题')     #标题
    cls = models.ForeignKey(to=ClassList,verbose_name='班级')       #问卷
    creator = models.ForeignKey(to=Userinfo,verbose_name='用户')    #用户id

    class Meta:
        verbose_name_plural= '问卷表'
    def __str__(self):
        return self.title

class Question(models.Model):
    '''
    问题表
    '''
    caption = models.CharField(max_length=64,verbose_name='标题')   #标题
    question_types = (
        (1,'打分'),
        (2,'单选'),
        (3,'评价')
    )
    tp = models.IntegerField(choices=question_types,verbose_name='回答方式')   #类型框
    naire = models.ForeignKey(to=Questionnaire,verbose_name="问卷")  #所属问卷

    class Meta:
        verbose_name_plural= '问题表'
    def __str__(self):
        return  self.caption

class Option(models.Model):
    '''
    单选题的选项表
    '''
    name = models.CharField(verbose_name='选项', max_length=32)     #名字
    score = models.IntegerField(verbose_name='分值')     #分值
    qs = models.ForeignKey(to=Question,verbose_name='问题')     #问题id

    class Meta:
        verbose_name_plural= '选项表'
    def __str__(self):
        return self.name

class Answer(models.Model):
    """
    回答表
    """
    stu = models.ForeignKey(to=Student)         #学生id
    question = models.ForeignKey(to=Question)   #问题id

    option = models.ForeignKey(to="Option",null=True,blank=True)    #单选题id
    val = models.IntegerField(null=True,blank=True)     #人数
    content = models.CharField(max_length=255,null=True,blank=True) #回答的内容

    class Meta:
        verbose_name_plural= '回答表'