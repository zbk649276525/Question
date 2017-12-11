from django.core.exceptions import ValidationError
from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from . import forms
from django.forms import ModelForm,widgets,fields,Form
from .forms import QuestionModelForm,Quest,OptionModelForm
import json
from django.core.exceptions import ValidationError
# Create your views here.


def login(request):
    '''
    用户登录
    :param request:
    :return:
    '''
    if request.method == "GET":
        return render(request,"login.html")
    else:
        #1.先设给状态值
        state= {'state':False, 'error_msg':None}
        #2. 获取值，判断
        user = request.POST.get('user')
        pwd = request.POST.get("pwd")
        # print(user)
        user_obj = models.Student.objects.filter(user=user,pwd=pwd).first()

        if user_obj:
            state["state"] = True
            request.session['username'] = user
            request.session['user_id']  = user_obj.id
            print(user_obj.id)
        # if not user_obj:
        #     state["error_msg"] = 'user_error'
        # if user == '':
        #     state["state"] = 'user_null'
        #     return HttpResponse(json.dumps(state))
        #
        # if pwd == '':
        #     state["state"] = 'pwd_null'
            return HttpResponse(json.dumps(state))

def index(request):
    '''
    主页
    :param request:
    :return:
    '''
    questionnaire = models.Questionnaire.objects.all()
    user = request.session.get('username')
    if request.method == "GET":
        return  render(request,'index.html',locals())
    else:
        print(user)
        return render(request, 'questionsadd.html', locals())

def questionsadd(request):
    '''
    添加问卷
    :param request:
    :return:
    '''
    if request.method == "GET":
        user = request.session['username']
        classlist = models.ClassList.objects.all()
        userinfo = models.Userinfo.objects.all()
        return render(request, "questionsadd.html",locals())
    else:
        title=request.POST.get("title")     #从前端获取到title
        cls = request.POST.get("cls")       #从前端获取到cls
        user_id = request.session.get("user_id")     #从前端获取到user
        print(user_id)
        models.Questionnaire.objects.create(title=title,cls_id=cls,creator_id=user_id)
        return redirect("/index/")

def questionnaire(request,nid):
    '''
    编辑问卷
    :param request:
    :param nid:
    :return:
    '''
    if request.method == "GET":
        def inner():
            question_list = models.Question.objects.filter(naire_id=nid)  #获取到当前问题对应的问卷
            if not question_list:
            #     print("====就不会走里面。")
                form = forms.QuestionModelForm()
                yield {"form":form, "obj":None, "option_cls":"hide", "options":None}
            else:
                for foo in question_list:
                    form = forms.QuestionModelForm(instance=foo) #针对当前的问题，foo值是一个对象
                    temp = {"form":form, "obj":foo , "option_cls":"hide", "options":None}
                    if foo.tp == 2:
                        temp["option_cls"] = ""

                        #获取当前问题的所有选项
                        def inner_foo(xxx):
                            option_list = models.Option.objects.filter(qs=xxx)
                            for v in option_list:
                                yield {"form":OptionModelForm(instance=v),"obj":v}

                        temp["options"] = inner_foo(foo)
                    yield  temp
        return render(request,"questionnaire.html",{"form_list":inner()})
    else:
        data = json.loads(request.body.decode("utf-8"))
        print(data,'===========')
        #获取当前问卷的所有问题
        question_list=models.Question.objects.filter(naire_id=nid)

        #获取当前用户提交所有问题的id
        post_id_list = [i.get("id") for i in data]
        print('111',post_id_list)

        #获取当前数据库中已有问题的id
        question_id_list = [str(i.id) for i in question_list]
        print(question_id_list)

        #利用集合去重，并且 获取需要删除的id
        del_id_list = set(question_id_list).difference(post_id_list);
        print(del_id_list)
        for i in del_id_list:
            models.Question.objects.filter(id=i).delete()

        for item in data:
            qid = item.get("id")
            print('qid',qid)
            caption = item.get("caption")
            tp = item.get("tp")
            options = item.get("options")

            #如果用户传过来的id不在数据库原有id列表中的时候，表示要新增
            if qid not in question_id_list:
                new_question_obj = models.Question.objects.create(caption=caption,tp=tp,naire_id=nid)
                if tp ==2:
                    for op in options:
                        models.Option.objects.create(qs=new_question_obj,name=op.get("name"),score=op.get("score"))

            #否则表示要更新
            else:
                models.Question.objects.filter(id=qid).update(caption=caption,tp=tp,naire_id=nid)
                if not options:  #如果没有选项表示要删除选项
                    models.Option.objects.filter(qs_id=int(qid)).delete()
                else:
                    models.Option.objects.filter(qs_id=int(qid)).delete()
                    for op in options:
                        print(op,'============================')
                        models.Option.objects.create(name=op.get("name"),score=op.get("score"),qs_id=qid)
    return HttpResponse('ok')

def func(content):
    if len(content)<15:
        raise ValidationError("长度不得少于15个字符")

def score(request,q_id,c_id):
    '''
    问卷里的问题————回答
    :param request:
    :param q_id:
    :param c_id:
    :return:
    '''
    stu_id=request.session.get("user_id")  #从session中取出当前登录用户的id
    if not stu_id:
        return redirect("/login/")

    #判断当前登录的用户是否需要答卷的班级的学生
    stu_obj = models.Student.objects.filter(id=stu_id,cls_id=c_id).count()
    if not stu_obj:
        return  HttpResponse("对不起，您不是本次调查的对象")

    #判断是否已经提交过问卷答案
    has_join = models.Answer.objects.filter(stu_id=stu_id,question__naire_id=q_id)
    if has_join:
        return HttpResponse("对不起，您已经参与本次问卷，不可重复参与")

    #获取当前问卷的所有问题
    question_list = models.Question.objects.filter(naire_id=q_id)
    field_dict = {}    #设一个空字典
    for que in question_list:   #for 循环取出所有问题
        if que.tp ==1:   #如果等于打分类型。
            field_dict["val_%s"%que.id] = fields.ChoiceField(
                label = que.caption,        #标题
                error_messages={"required":"必填"},   #提示错误
                widget = widgets.RadioSelect,   #单选圆点
                choices=[(i,i) for i in range (1,11)]   #循环1-11
            )
        elif que.tp ==2:
            field_dict["option_id_%s"%que.id] = fields.ChoiceField(
                label = que.caption,    #标题
                error_messages={"required":"必填"},   #错误提示
                widget = widgets.RadioSelect,   #单选圆点
                #这里数据表option中的score是不需要给用户看到的
                choices = models.Option.objects.filter(qs_id=que.id).values_list("id","name")   #按需求取需要的值
            )
        else:
            field_dict["content_%s"%que.id] = fields.CharField(
                label = que.caption,    #标题
                error_messages={"required":"必填"},   #错误提示
                widget = widgets.Textarea(attrs={"class":"form-control","rows":"2","cols":"60"}),   #输入文本框
                validators = [func,]  #这里可以写正则，也可以自定义函数放在这里
            )
    myForm = type("myTestForm",(Form,),field_dict)   #动态生成类，参数分别是类名，继承的对象，字段

    if request.method == "GET":
        form = myForm()     #实例化
        return  render(request,"score.html",{"question_list":question_list,"form":form})
    else:
        form = myForm(request.POST)
        if form.is_valid():     #验证成功
            obj_list = []       #设个空立标
            for key,v in form.cleaned_data.items():     #  for 循环干净数据。
                print('zzzzzzzzzzzzzzzzzzzzz',key,v)     # val_5  2
                key,qid = key.rsplit("_",1) #从右边切，切一次
                print(key,qid)      #val 5
                answer_dict = {"stu_id":stu_id, "question_id":qid,key:v}  #上面切分成根数据库对应的格式，以便我们保存。
                print(answer_dict)
                obj_list.append(models.Answer(**answer_dict))
            models.Answer.objects.bulk_create(obj_list)  #批量插入
            return HttpResponse("感谢您的参与")
        return render(request,"score.html",{"question_list":question_list,"form":form})










