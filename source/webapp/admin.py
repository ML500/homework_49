from django.contrib import admin
from webapp.models import Goal, Status, Type, GoalType


class GoalAdmin(admin.ModelAdmin):
    pass


admin.site.register(Goal, GoalAdmin)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(GoalType)
