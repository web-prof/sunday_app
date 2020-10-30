from django import forms
from .models import *


class Exam_form(forms.Form):
    question = forms.CharField(widget=forms.TextInput(attrs={
        "name": "question",
        "class": "form-control",
        "id": "question",
        "placeholder": "السؤال",

    }))
    answer1 = forms.CharField(widget=forms.TextInput(attrs={
        "name": "answer1",
        "class": "form-control",
        "id": "answer1",
        "placeholder": "الاختيار الاول",

    }))
    answer2 = forms.CharField(widget=forms.TextInput(attrs={
        "name": "answer2",
        "class": "form-control",
        "id": "answer2",
        "placeholder": "الاختيار الثانى",

    }))
    answer3 = forms.CharField(widget=forms.TextInput(attrs={
        "name": "answer3",
        "class": "form-control",
        "id": "answer3",
        "placeholder": "الاختيار الثالث",

    }))
    answer4 = forms.CharField(widget=forms.TextInput(attrs={
        "name": "answer4",
        "class": "form-control",
        "id": "answer4",
        "placeholder": "الاختيار الرابع",

    }))
    correct_answer = forms.CharField(widget=forms.TextInput(attrs={
        "name": "correct_answer",
        "class": "form-control",
        "id": "correct_answer",
        "placeholder": "الاجابه الصحيحه",

    }))


class prof_image_form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
