from django.db import models
from accounts.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    prompt = models.CharField(max_length=500)
    point = models.FloatField()
    secret_code = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class YTTasker_task(models.Model):
    tasker = models.ForeignKey(User,  on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.tasker} - {self.task}'

    @receiver(post_save, sender=Task)
    def create_yttasker_task(sender, instance, created, **kwargs):
        users = User.objects.all()
        if created:
            for user in users:
                YTTasker_task.objects.create(tasker=user, task=instance)

class Notification(models.Model):
    info = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.info
    

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()

    def __str__(self):
        return self.question