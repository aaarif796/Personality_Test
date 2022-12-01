from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey

# Create your models here.
class wordSentiment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField(error_messages = {
                 'required':"Please Enter the Text"
                 })
    date=models.DateField()
    result=models.CharField(max_length=12)
    def __str__(self):
        return self.result

class p_testd(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    p_text=models.TextField(error_messages = {
                 'required':"Please Enter the Text"
                 })
    date=models.DateField()
    p_result=models.CharField(max_length=12)
    
    def __str__(self):
        return self.p_result

class t_testd(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    t_text=models.TextField(error_messages = {
                 'required':"Please Enter the Text"
                 })
    date=models.DateField()
    t_result=models.CharField(max_length=12)
    def __str__(self):
        return self.t_result