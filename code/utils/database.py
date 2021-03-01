from django.db.models import QuerySet
import pymysql


def fetchall_2_dict(cursor: pymysql.cursors.Cursor):
    """
    将pymysql游标返回的结果保存到一个字典对象中
    """
    return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]


def values_list_ids(queryset: QuerySet) -> QuerySet:
    return queryset.values_list('id', flat=True)


def values_list_ids_set(queryset: QuerySet) -> set:
    return set(values_list_ids(queryset))


ids_set = values_list_ids_set
