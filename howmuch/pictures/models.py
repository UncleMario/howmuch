# -*- encoding: utf-8 -*-
import os
import uuid
from django.db import models
from howmuch.pictures.thumbs import ImageWithThumbsField
from django.contrib.auth.models import User
from django.conf import settings

def make_upload_path(instance, filename): ##Autor: msamoylov by Stackoverflow
    file_root, file_ext = os.path.splitext(filename)
    dir_name = '{module}/{model}'.format(module=instance._meta.app_label, model=instance._meta.module_name)
    file_root = unicode(uuid.uuid4())
    name = os.path.join(settings.MEDIA_ROOT, dir_name, file_root + file_ext.lower())

    # Delete existing file to overwrite it later

    if instance.pk:
        while os.path.exists(name):
            os.remove(name)

    return os.path.join(dir_name, file_root + file_ext.lower())

class Picture(models.Model):
	picture = ImageWithThumbsField(upload_to=make_upload_path, sizes=((100,100),(250,250),(250,500),(200,450),(300,450),(250,400),(500,250),(450,200)))
	owner = models.ForeignKey(User)
	date = models.DateTimeField(auto_now=True, auto_now_add=True)

	def __unicode__(self):
			return self.picture.url







