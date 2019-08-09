from django.utils.translation import gettext as _

# Reusable Choices fields which can be imported at models.py and forms.py
STATUS_CHOICES = (
    ('To Do', _('To Do')),
    ('In Progress', _('In Progress')),
    ('Blocked', _('Blocked')),
    ('Done', _('Done')),
    ('Dismissed', _('Dismissed'))
)

PRIORITY_CHOICES = (
    ('Low', _('Low')),
    ('Normal', _('Normal')),
    ('High', _('High')),
    ('Critical', _('Critical')),
    ('Blocker', _('Blocker'))
)
