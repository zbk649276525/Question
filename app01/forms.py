from django import forms
from . import models
from django.forms import Form,fields,widgets,ModelForm

class Quest(Form):
    title = forms.CharField(
        required=True,
        max_length=32,
        error_messages={"required":"不能为空"},
        widget=widgets.TextInput(attrs={"placeholder":"请输入问题","class":"form-control","id":"title"})
    )
    choice = forms.CharField(
        required=True,
        max_length=16,
        error_messages={"required":"不能为空"},
        widget=widgets.Select(attrs={"class":"form-control"})
    )

class QuestionModelForm(ModelForm):
    class Meta:
        model = models.Question     #帮Question里面所有字段都可以拿到
        fields = "__all__"  #拿到个人的字段  但如果是 "__all__" 就表示所有的字段
        error_messages = {
            "caption":{"required0":"名称不能为空"}
        }
        widgets = {
            "caption":widgets.Textarea(attrs={
                "class":"form-control",
                "style":"resize:none; width:500px; height:40px;"
            }),
            "tp":widgets.Select(attrs={"class":"form-control","id":"select_change"})
        }

class OptionModelForm(ModelForm):
    class Meta:
        model = models.Option
        fields = ['name','score']
        widgets = {
            "name":widgets.TextInput(attrs={"class":"form-control"}),
            "score":widgets.TextInput(attrs={"class":"form-control"}),
        }
















