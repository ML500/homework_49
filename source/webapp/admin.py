from django.contrib import admin
from webapp.models import Goal, Status, Type, Project


class GoalAdmin(admin.ModelAdmin):
    filter_horizontal = ('type',)


admin.site.register(Goal, GoalAdmin)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Project)
