import django_tables2 as tables

from .models import Task


class TaskTable(tables.Table):
    """ User django_tables2 library to create a quick bootstrap table
        having dynamic action column to view task. This is used to show search results. """
    action = tables.TemplateColumn("<a href='{{ record.get_absolute_url }}' class='btn btn-primary'>View</a>",
                                   orderable=False,
                                   )

    class Meta:
        model = Task
        fields = ('title', 'status', 'priority', 'created_date', 'action')
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {'class': 'table table-striped table-hover'}
        order_by = '-created_date'
