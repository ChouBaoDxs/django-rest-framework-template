from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', null=True)
    like_count = models.IntegerField('like count', default=0)

    # 注意：如果字段里有 choices 参数，Serializer 会转为 ChoiceField，django_socio_grpc 的 get_proto_type 方法会识别成 string 类型，导致类型对应失败，所以不能写 choices
