from django.db import models

class Portofolio(models.Model):
    name = models.CharField(max_length=128)

class Member(models.Model):
    name = models.CharField(max_length=128)
    rank = models.CharField(max_length=128)
    url = models.CharField(max_length=512)
    photoUrl = models.CharField(max_length=512)
    portofolio = models.ForeignKey(Portofolio)

class Meeting(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=512)
    member = models.ForeignKey(Member)
    lobby = models.BooleanField(default=False)
