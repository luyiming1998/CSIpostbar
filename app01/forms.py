from django.forms import Form, fields, widgets
from django.core.exceptions import ValidationError
from .models import *


class RegForm(Form):
    regusername = fields.CharField()
    regpassword = fields.CharField()
    regsex = fields.IntegerField()
    regAge = fields.IntegerField()
    regEmail = fields.EmailField()

    def clean_regAge(self):
        val=self.cleaned_data.get("regAge")
        if 0<=val<=100:
            return val
        else:
            raise ValidationError("年龄必须在0-100之间")

    def clean_regusername(self):
        val=self.cleaned_data.get("regusername")
        user=User.objects.filter(userName=val).first()
        if user:
            raise ValidationError("该用户名已被注册")
        else:
            return val