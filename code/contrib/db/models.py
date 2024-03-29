from django.db import models
from django.utils import timezone


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


class LogicDeleteQuerySet(models.QuerySet):
    def delete(self):  # queryset 的逻辑删除方法
        # return self.update(is_deleted=True, deleted_at=timezone.now())
        return self.update(deleted_at=timezone.now())


class LogicDeleteManager(models.manager.BaseManager.from_queryset(LogicDeleteQuerySet)):
    pass


class LogicDeleteModel(models.Model):
    # is_delete = models.BooleanField('删除标记', default=False, editable=False)
    deleted_at = models.DateTimeField('删除时间', null=True, db_index=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):  # 单个实例的逻辑删除方法
        # self.is_delete = True
        self.deleted_at = timezone.now()
        # self.save(update_fields=['is_delete', 'deleted_at'])
        self.save(update_fields=['deleted_at'])

    class NotDeleteManager(LogicDeleteManager):
        def get_queryset(self):
            # return super().get_queryset().filter(is_delete=False)
            return super().get_queryset().filter(deleted_at__isnull=True)

    objects = NotDeleteManager()
    all_objects = models.Manager()  # 需要查找被逻辑删除的数据时使用这个 all_objects


class ReadOnlyModel(BigIntPkModel, CreatedAtModel):
    class Meta:
        abstract = True


class GenericModel(BigIntPkModel, DateTimeRecordModel, LogicDeleteModel):
    class Meta:
        abstract = True
