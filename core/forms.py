from django import forms
from .models import *


class Exam_form(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        exclude = ['t_class']

