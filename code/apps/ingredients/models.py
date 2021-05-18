from django.db import models


class Category(models.Model):
    name = models.CharField('类别名称', max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('成分', max_length=100)
    notes = models.TextField('备注')
    category = models.ForeignKey(Category, verbose_name='类别', related_name="ingredients", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
