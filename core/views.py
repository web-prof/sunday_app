from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required


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


def log_out(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='/')
def profile(request):
    prof = Profile.objects.get(user=request.user)
    profs = Profile.objects.filter(p_class=prof.p_class).exclude(user__is_staff=True).exclude(score=0).order_by('-score')[0:10]
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
    exam = Exam.objects.filter(t_class=prof.p_class).exclude(
        question__in=results.values_list('question_ans', flat=True))

    return render(request, 'profile.html', {'prof': prof, 'exam': exam, 'profs': profs})


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
def exam_crud(request):
    p = Profile.objects.get(user=request.user)
    exam = Exam.objects.filter(t_class=p.p_class).order_by('-last_update')
    if request.method == 'POST':
        form = Exam_form(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.t_class = p.p_class
            myform.save()
            return redirect('core:exam_crud')
    else:
        exam_form = Exam_form()
        return render(request, 'exam_crud.html', {'exam_form': exam_form, 'exam': exam})


@staff_member_required()
def delete_exam(request, id):
    exam = Exam.objects.get(id=id)
    exam.delete()
    return redirect('core:exam_crud')

