from django.contrib.auth.models import User
from django.db import models

from contrib.db.models import GenericModel


class UserProfile(GenericModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT, db_constraint=False, editable=False, null=True)
    phone = models.CharField('phone', max_length=32, null=True, unique=True)
    desc = models.TextField('desc', default='', blank=True)

    class Meta:
        verbose_name = verbose_name_plural = '用户信息'
