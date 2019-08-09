from django.contrib import admin

from .models import Task, Comment


# Register admin models here.
class CommentLine(admin.TabularInline):
    """ comments model for admin """
    model = Comment
    extra = 0


class TaskAdmin(admin.ModelAdmin):
    """ show comments inline to Task for admin """
    inlines = [CommentLine]


# finally register
admin.site.register(Comment)
admin.site.register(Task, TaskAdmin)
