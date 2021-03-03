import xadmin

from .models import (
    UserProfile,
)


@xadmin.sites.register(UserProfile)
class UserProfileAdmin(object):
    list_display = ['id', 'user', 'phone']
    relfield_style = 'fk-ajax'
    list_filter = ['user', 'created_at', 'updated_at']
    search_fields = ['user__username', 'phone']
    style_fields = {'user': "fk-ajax"}
