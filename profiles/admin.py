from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from profiles.models import User, Requests, Friends, Interest, UserInterest

class UserAdmin(admin.ModelAdmin):
	model = User
	filter_horizontal = ('user_permissions', 'groups',)
admin.site.register(User, UserAdmin)
# Register your models here.

admin.site.register(Requests)
admin.site.register(Friends)
admin.site.register(Interest)
admin.site.register(UserInterest)
