from django.db import models


class BigIntPkModel(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField('创建时间', auto_now_add=True, db_index=True)

    class Meta:
        abstract = True


class DateTimeRecordModel(models.Model):
    created_at = models.DateTimeField('创建时间', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True, db_index=True)

    class Meta:
        abstract = True


class LogicDeleteModel(models.Model):
    is_delete = models.BooleanField('删除标记', default=False, editable=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save(update_fields=['is_delete'])

    class NotDeleteManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_delete=False)

    objects = NotDeleteManager()
    all_objects = models.Manager()


class ReadOnlyModel(BigIntPkModel, CreatedAtModel):
    class Meta:
        abstract = True


class GenericModel(BigIntPkModel, DateTimeRecordModel, LogicDeleteModel):
    class Meta:
        abstract = True
