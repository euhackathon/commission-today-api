from django.db import models

class Portofolio(models.Model):
    name = models.CharField(max_length=128)
    shorthand = models.CharField(max_length=128, default='')
    def __unicode__(self):
        if self.shorthand:
            return self.shorthand
        return self.name

class Member(models.Model):
    name = models.CharField(max_length=128)
    rank = models.CharField(max_length=128)
    url = models.CharField(max_length=512)
    photoUrl = models.CharField(max_length=512)
    portofolio = models.ForeignKey(Portofolio)
    def __unicode__(self):
        return self.name

class Organization(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    money = models.IntegerField(null=True, blank=True)
    lobbyists = models.IntegerField(null=True, blank=True)
    registered = models.BooleanField(default=False, blank=True)
    explore_url = models.CharField(max_length=128, blank=True)
    def __unicode__(self):
        return self.name

class Meeting(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=512)
    member = models.ForeignKey(Member)
    lobby = models.BooleanField(default=False)
    # TODO: @palcu make a many to many relationship
    organization = models.ForeignKey(Organization, null=True)
    def __unicode__(self):
        return self.description
