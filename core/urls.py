from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', log_in, name='log_in'),
    path('logo_out/', log_out, name='log_out'),
    path('profile/', profile, name='profile'),
    path('prof_image/', prof_image, name='prof_image'),
    path('staff_panel/', staff_panel, name='staff_panel'),
    path('user_crud/',user_crud,name='user_crud'),
    path('delete_user/<int:id>',delete_user,name='delete_user'),
    path('exam_crud/',exam_crud,name='exam_crud'),
    path('delete_exam/<int:id>',delete_exam,name='delete_exam'),
    path('export_data/', file_load_view, name='export_data'),
    path('publish_questions/',publish_questions,name='publish_questions'),



]
