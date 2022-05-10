from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import BackgroundStudy, Course, CourseGroup, File, Registration, Student, Teacher
User = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'fullname','is_staff']
    list_filter = ['admin']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('fullname',)}),
        ('Permissions', {'fields': ('staff','admin','is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(File)
admin.site.register(Student)

class BackgAdmin(admin.ModelAdmin):
    list_display = ('id','major', 'school')

# Register the admin class with the associated model
admin.site.register(BackgroundStudy, BackgAdmin)

admin.site.register(Course)
class CourseGAdmin(admin.ModelAdmin):
    list_display = ('groupname', 'course','teacher')

# Register the admin class with the associated model
admin.site.register(CourseGroup, CourseGAdmin)

admin.site.register(Teacher)

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'courseGroup')

# Register the admin class with the associated model
admin.site.register(Registration, RegistrationAdmin)
