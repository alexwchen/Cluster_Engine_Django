from django.db import models

class list_object(models.Model):
    title = models.CharField(max_length=200)
    def __unicode__(self):
        return self.title

class object_object(models.Model):
    title = models.CharField(max_length=200)
    master_list = models.ForeignKey(list_object)
    def __unicode__(self):
        return self.title

class parameter_object(models.Model):
    title = models.CharField(max_length=200)
    default = models.IntegerField(default=0)
    master_object = models.ForeignKey(object_object)
    def __unicode__(self):
        return self.title


class Document(models.Model):
    title = models.CharField(max_length=200)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    def __unicode__(self):
        return self.title
