from django.db import models

class Portofolio(models.Model):
    name = models.CharField(max_length=128)
