from django.contrib import admin
from .models import Student, Parent, Tutor, Group
# Register your models here.
# admin.site.register()

admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Tutor)
admin.site.register(Group)