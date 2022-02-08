from django.db import models
from django.utils import timezone

# Create your models here.
class ProjectDD(models.Model):
    create_time = models.DateTimeField(default = timezone.now)
    puser = models.CharField(max_length=60)
    pname = models.CharField(max_length=60)
    pnum = models.CharField(max_length=60)
    pcate = models.CharField(max_length=60)
    plevel = models.CharField(max_length=60)
    pmanager = models.CharField(max_length=60)
    ppay = models.CharField(max_length=60)
