from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views

app_name = 'task'

# define all url patters/routes for the app with namespace 'task'
urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("register/", views.register, name="register"),
    re_path(r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$", views.activate,
            name="activate"),
    path("accounts/password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("accounts/password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("accounts/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("accounts/reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("password/", views.change_password, name="change_password"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/createtask/", views.create_task, name="createtask"),
    path("dashboard/task_detail/<int:task_id>", views.task_detail, name="task_detail"),
    path("dashboard/edittask/<int:task_id>", views.edit_task, name="edittask"),
    path("dashboard/deletetask/<int:task_id>", views.delete_task, name="deletetask"),
    path("dashboard/deletecomment/<int:comment_id>", views.delete_comment, name="deletecomment"),
    path('dashboard/taskactivity', views.taskactivity, name='taskactivity'),
    path('dashboard/chartdata', views.chartdata, name='chartdata'),
    path('dashboard/search_results', views.search, name='search'),
    path('dashboard/taskdetail/<int:task_id>/comment/', views.add_comment_to_task, name='add_comment_to_task'),
]
