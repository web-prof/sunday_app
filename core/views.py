from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required
# import csv
from django.http import HttpResponse
import xlwt


# import unicodecsv

def log_in(request):
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        re = auth.authenticate(username=u, password=p)
        if re is not None:
            auth.login(request, re)
            if request.user.is_staff:
                return redirect('core:staff_panel')
            return redirect('core:profile')
        else:
            messages.warning(request, 'اسم المستخدم او الرقم السرى غير صحيح')
            return redirect('/')
    else:
        return render(request, 'login.html', {})

@login_required(login_url='/')
def log_out(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='/')
def profile(request):
    prof = Profile.objects.get(user=request.user)
    profs = Profile.objects.filter(p_class=prof.p_class).exclude(user__is_staff=True).exclude(score=0).order_by(
        '-score')[0:10]
    exam = Exam.objects.filter(t_class=prof.p_class)
    if request.method == 'POST':
        for m in exam:
            if request.POST.get(m.question, ) == m.correct_answer:
                results = Results.objects.create(
                    profile=prof,
                    question_ans=m.question,
                    student_ans=request.POST.get(m.question, ),
                    correct_ans=m.correct_answer,
                    is_correct=True,
                )
                results.save()
                prof.score += 1
                prof.save()
            else:
                results = Results.objects.create(
                    profile=prof,
                    question_ans=m.question,
                    student_ans=request.POST.get(m.question, ),
                    correct_ans=m.correct_answer,
                    is_correct=False,
                )

        return redirect('core:profile')

    else:
        results = Results.objects.filter(profile=prof)
        # for quest in exam:
        #     for res in results:
        #
    form=prof_image_form()
    exam = Exam.objects.filter(t_class=prof.p_class, is_published=True).exclude(
        question__in=results.values_list('question_ans', flat=True))

    return render(request, 'profile.html', {'prof': prof, 'exam': exam, 'profs': profs,'form':form})

@login_required(login_url='/')
def prof_image(request):
    prof = Profile.objects.get(user=request.user)
    form = prof_image_form(request.POST, request.FILES, instance=prof)
    if form.is_valid():
        form.save()

    return redirect('core:profile')

@staff_member_required()
def staff_panel(request):
    return render(request, 'staff_panel.html', {})


@staff_member_required()
def user_crud(request):
    p = Profile.objects.get(user=request.user)
    profile = Profile.objects.filter(p_class=p.p_class).exclude(user__is_staff=True).order_by('-last_update')
    if request.method == 'POST':
        u = request.POST['username']
        p1 = request.POST['password1']
        p2 = request.POST['password2']
        if User.objects.filter(username=u).exists():
            messages.info(request, 'تاكد من عدم تكرار اسم المستخدم')
            return redirect('core:user_crud')
        elif u == "":
            messages.info(request, 'من فضلك قم باضافة اسم للمستخدم')
            return redirect('core:user_crud')
        elif p1 != p2:
            messages.info(request, 'تاكد من ان الرقم السري وتاكيد الرقم السري متطابقين ')
            return redirect('core:user_crud')
        elif len(p1) < 8:
            messages.info(request, 'عفوا الرقم السري يجب ان لايقل عن 8 عناصر  ')
            return redirect('core:user_crud')
        else:
            user = User.objects.create_user(username=u, password=p1)
            user.save()
            k = Profile.objects.get(user=user)
            k.p_class = p.p_class
            k.save()

            return redirect('core:user_crud')
    else:
        return render(request, 'user_crud.html', {'prof': profile})


@staff_member_required()
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('core:user_crud')


@staff_member_required()
def file_load_view(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="student.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Student')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['اسم المستخدم', 'الدرجات', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    p = Profile.objects.get(user=request.user)
    rows = Profile.objects.filter(p_class=p.p_class).exclude(user__is_staff=True).order_by(
        '-last_update').values_list('user__username', 'score')
    # rows = StudentForm.objects.all().values_list('firstname', 'lastname', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


# def file_load_view(request):
#     p = Profile.objects.get(user=request.user)
#     p1 = Profile.objects.filter(p_class=p.p_class).exclude(user__is_staff=True).order_by(
#         '-last_update').values_list('user__username', flat=True)
#     p2 = Profile.objects.filter(p_class=p.p_class).exclude(user__is_staff=True).order_by(
#         '-last_update').values_list('score', flat=True)
#     # Create the HttpResponse object with the appropriate CSV header.
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="students_name.csv"'
#
#     # writer = unicodecsv.writer(response, encoding='utf-16"')
#     writer = csv.writer(response)
#
#     writer.writerow(['username', 'score'])
#     rows = zip(p1, p2)
#     for m in rows:
#         writer.writerow(m)
#
#     return response


@staff_member_required()
def exam_crud(request):
    p = Profile.objects.get(user=request.user)
    exam = Exam.objects.filter(t_class=p.p_class).order_by('-last_update')
    if request.method == 'POST':
        form = Exam_form(request.POST)
        if form.is_valid():
            exam_form = Exam.objects.create(
                t_class=p.p_class,
                question=form.cleaned_data['question'],
                answer1=form.cleaned_data['answer1'],
                answer2=form.cleaned_data['answer2'],
                answer3=form.cleaned_data['answer3'],
                answer4=form.cleaned_data['answer4'],
                correct_answer=form.cleaned_data['correct_answer'],
                is_published=False,
            )
            exam_form.save()
            # myform = form.save(commit=False)
            # myform.t_class = p.p_class
            # myform.save()
            return redirect('core:exam_crud')
        else:
            messages.info(request, 'من فضلك تاكد من مليء جميع الحقول')
            return redirect('core:exam_crud')
    else:
        exam_form = Exam_form()
        return render(request, 'exam_crud.html', {'exam_form': exam_form, 'exam': exam})


def publish_questions(request):
    p = Profile.objects.get(user=request.user)
    exam = Exam.objects.filter(t_class=p.p_class, is_published=False).order_by('-last_update')
    for m in exam:
        m.is_published = True
        m.save()
    return redirect('core:exam_crud')


@staff_member_required()
def delete_exam(request, id):
    exam = Exam.objects.get(id=id)
    exam.delete()
    return redirect('core:exam_crud')
