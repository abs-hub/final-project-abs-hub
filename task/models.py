from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from task.choices import *


# Create your models here.

class Task(models.Model):
    """ Task model is the Master which holds all task information like title, status,
        priority, etc. It has two foreign key user and created_by """
    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='To Do', )
    priority = models.CharField(_("priority"), max_length=20, choices=PRIORITY_CHOICES, default='Normal')
    description = models.TextField(_("description"), max_length=2000, null=True, blank=True)
    resolution = models.TextField(_("resolution"), max_length=2000, null=True, blank=True)
    deadline = models.DateField(_("deadline"), null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks_assigned', verbose_name=_('assigned to'),
                             on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks_created', verbose_name=_('created by'),
                                   on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_("last modified"), auto_now=True, editable=False)

    def __str__(self):
        return "[%s] %s" % (self.id, self.title)

    def get_absolute_url(self):
        return reverse('task:task_detail', kwargs={'task_id': self.id})


class Comment(models.Model):
    """ Comment model is a child to Task (1 to many relationship). Has foreign key to user."""
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment_description = models.CharField(_("comment"), max_length=255)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_comments', verbose_name=_('created by'),
                               on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.comment_description
