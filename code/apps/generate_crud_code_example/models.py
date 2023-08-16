from django.contrib.auth.models import User
from django.db import models

from contrib.db.models import GenericModel


class BookKind:
    BOOK = 1
    MAGAZINE = 2


BookKind2Label = {
    BookKind.BOOK: '书籍',
    BookKind.MAGAZINE: '杂志',
}


class Book(GenericModel):
    creator = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False, editable=False, null=True)
    name = models.CharField('名称', max_length=32, blank=True)
    desc = models.TextField('描述', default='', blank=True)
    kind = models.PositiveSmallIntegerField(
        '类型',
        choices=BookKind2Label.items(),
        default=BookKind.BOOK,
        help_text=f'{BookKind2Label}',
    )

    class Meta:
        verbose_name = verbose_name_plural = '书籍'
