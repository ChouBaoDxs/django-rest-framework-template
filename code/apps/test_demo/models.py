from django.db import models


class TestListSerializerUnique(models.Model):
    code = models.CharField(unique=True, max_length=32)
