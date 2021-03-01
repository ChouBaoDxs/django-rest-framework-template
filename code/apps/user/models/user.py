from django.contrib.auth.models import User, Group
from django.db import models

from utils.base_class import GenericModel


class UserProfile(GenericModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT, db_constraint=False, null=True)
    phone = models.CharField('phone', max_length=32, null=True, unique=True, blank=True)
    desc = models.TextField('desc', default='', blank=True)

    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = verbose_name
