from django.db import models


class GoodsTag(models.Model):
    class Meta:
        verbose_name = '商品标签'
        db_table = 'goods_tag'

    name = models.CharField('标签名称', max_length=64)


class Goods(models.Model):
    class Meta:
        verbose_name = '商品'
        db_table = 'goods'

    name = models.CharField('商品名称', max_length=64)
    tags = models.ManyToManyField(GoodsTag, related_name='goods', verbose_name='标签')
