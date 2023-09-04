from django.db import models


class TestListSerializerUnique(models.Model):
    code = models.CharField(unique=True, max_length=32)


# 杭州公钥科技 boss 聊天编程题
class Category(models.Model):
    """ 分类表"""
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Product(models.Model):
    """ 产品表"""
    name = models.CharField(max_length=128, )
    category = models.ForeignKey(Category, null=True, default=None, on_delete=models.SET_NULL)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

"""
需求：
1.使用原生sql获取产品名称和其所属的分类名称，假设产品ID为1
    SELECT
        product.id,
        product.name,
        category.name AS 'category_name' 
    FROM
        product
        LEFT JOIN category ON product.category_id = category.id 
    WHERE
        product.id = 1 
        LIMIT 1

2.实现产品列表API,返回数据格式如下：
[
    {'id': 1,
     'name': 'product 1',
     'category': {'id': 1, 'name': 'category1'}
    },
    {'id': 2,
     'name': 'product 2',
     'category': {'id': 1, 'name': 'category1'}
    },
    {'id': 3,
     'name': 'product 3',
     'category': {'id': 2, 'name': 'category2'}
    }
    ...
]
通过 django + drf（尽量使用）或者django实现该API。
"""