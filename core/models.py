from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError

the_class = (
    ('الصف الاول', 'الصف الاول'),
    ('الصف الثانى', 'الصف الثانى'),
    ('الصف الثالث', 'الصف الثالث'),
    ('الصف الرابع', 'الصف الرابع'),
    ('الصف الخامس', 'الصف الخامس'),
    ('الصف السادس', 'الصف السادس'),

)


def validate_date(date):
    if date > timezone.now().date():
        raise ValidationError("Date cannot be in the future")


def image_upload(instance, filename):
    imagename, extension = filename.split(".")
    return "core/%s.%s" % (instance.id, extension)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload, null=True, blank=True)
    p_class = models.CharField(max_length=50, choices=the_class)
    score=models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now_add=timezone.now(), null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_student_score(self):
        prof = Profile.objects.get(user=self.user)
        res = Results.objects.filter(profile=prof, is_correct=True)
        if res.exists():
            return res.count()
        else:
            return 0

    # def get_score(self):
    #     dd = Profile.objects.filter()
    #     for p in dd:
    #         p['score'] = self.get_student_score
    #         dd.save()
    #     return dd


@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Results(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question_ans = models.CharField(max_length=100)
    student_ans = models.CharField(max_length=100, null=True, blank=True)
    correct_ans = models.CharField(max_length=100)
    is_correct = models.BooleanField()

    def __str__(self):
        return str(self.profile)



z_class = (
    ('الصف الاول', 'الصف الاول'),
    ('الصف الثانى', 'الصف الثانى'),
    ('الصف الثالث', 'الصف الثالث'),
    ('الصف الرابع', 'الصف الرابع'),
    ('الصف الخامس', 'الصف الخامس'),
    ('الصف السادس', 'الصف السادس')

)


class Exam(models.Model):
    t_class = models.CharField(max_length=50, choices=z_class)
    question = models.CharField(max_length=100)
    answer1 = models.CharField(max_length=100)
    answer2 = models.CharField(max_length=100)
    answer3 = models.CharField(max_length=100)
    answer4 = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)
    last_update = models.DateTimeField(auto_now_add=timezone.now(), null=True, blank=True)

    def __str__(self):
        return self.question
