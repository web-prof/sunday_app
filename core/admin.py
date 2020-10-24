from django.contrib import admin
from .models import *



class profileInline(admin.ModelAdmin):
    list_display = ['user', 'p_class']


admin.site.register(Profile, profileInline)


class examInline(admin.ModelAdmin):
    list_display = ['t_class', 'question']


admin.site.register(Exam, examInline)


class result_admin(admin.ModelAdmin):
    list_display = ['profile', 'question_ans', 'student_ans', 'correct_ans', 'is_correct']


admin.site.register(Results, result_admin)
