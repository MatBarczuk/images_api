from django.contrib import admin

from users.models import CustomUser


class CustomUserDashboard(admin.ModelAdmin):
    list_display = ('id', 'username', 'tier')
    list_editable = ('tier', )
    list_display_links = ('id', 'username')


admin.site.register(CustomUser, CustomUserDashboard)

admin.site.site_header = 'Admin Panel'
admin.site.site_title = 'Image Resizer'
admin.site.index_title = 'Administration'
