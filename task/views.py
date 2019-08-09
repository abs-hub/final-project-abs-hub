import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django_tables2 import RequestConfig

from .forms import SignupForm, UserLoginForm, TaskForm, CommentForm
from .models import Task, Comment
from .tables import TaskTable
from .token import account_activation_token


def home(request):
    """ Home page for the application, if user is logged in redirect to dashboard
        else show welcome page."""
    if request.user.is_authenticated:
        return redirect('task:dashboard')

    return render(request, 'management/home.html')


def log_in(request):
    """ login view when user goes on login route """
    if request.user.is_authenticated:
        return redirect('task:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Grab username & password submitted via POST request
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # call Django's built in username and password authentication
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('task:dashboard')
            else:
                return render(request, 'management/login.html', {'form': form, 'user': user})
    else:
        form = UserLoginForm
    context = {'form': form}
    return render(request, 'management/login.html', context)


def log_out(request):
    """
        Log out user.
    """
    logout(request)
    return redirect('task:home')


def register(request):
    """
        Register new user.
    """
    if request.user.is_authenticated:
        return redirect('task:dashboard')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # do captcha validation by calling google's siteverify API
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''
            # if response is success send activation email by user the credentials stored in settings.py
            if result['success']:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('management/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                try:
                    email.send()
                except Exception as e:
                    print(e)
                # send response to user
                return HttpResponse('An activation Link has been sent to your email address.Please Check your Inbox')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
    else:
        form = SignupForm()

    context = {'form': form}
    return render(request, 'management/register.html', context)


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    """ this view handles route when user clicks activation link from the email """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Thank you for your email confirmation. Now you have logged In')
        return redirect('task:dashboard')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='/login')
def change_password(request):
    """change password view """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('task:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'management/change_password.html', {'form': form})


@login_required(login_url='/login')
def dashboard(request):
    """ home page for logged in user """
    user = request.user
    tasks = Task.objects.filter(user=user)
    context = {
        'tasks': tasks,
    }
    return render(request, 'management/dashboard.html', context)


@login_required(login_url='/login')
def create_task(request):
    """ handles create task request when post else
        would render TaskForm """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('task:task_detail', task_id=task.pk)
        else:
            return redirect('task:dashboard')
    else:
        form = TaskForm()
    context = {'form': form}
    return render(request, 'management/createtask.html', context)


@login_required(login_url='/login')
def delete_task(request, task_id):
    """ delete task view """
    task = get_object_or_404(Task, pk=task_id)
    """ Doing server side validation instead of client side 
        due to security reason of exposing the delete_task function """
    if task.user == request.user or request.user.is_superuser:
        task.delete()
    else:
        messages.error(request, 'You can delete only your own task.')
    return redirect('task:dashboard')


@login_required(login_url='/login')
def add_comment_to_task(request, task_id):
    """ add comment to task and redirect to task detail """
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect('task:task_detail', task_id=task_id)
    else:
        return redirect('task:task_detail', task_id=task_id)


@login_required(login_url='/login')
def delete_comment(request, comment_id):
    """ delete comment view
        super user or original commenter are allowed to delete comments """
    comment = get_object_or_404(Comment, pk=comment_id)
    """ Doing server side validation instead of client side 
        due to security reason of exposing the delete_comment function """
    if comment.author == request.user or request.user.is_superuser:
        comment.delete()
    else:
        messages.error(request, 'You can delete only your own task.')
    return redirect('task:task_detail', task_id=comment.task.pk)


@login_required(login_url='/login')
def edit_task(request, task_id):
    """ edit task view
        super users can edit any task and
        if logged in user is owner they are also allowed to edit """
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        if task.user == request.user or request.user.is_superuser:
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                task = form.save(commit=False)
                # user is required to fill out resolution while completing the task
                if task.status == "Done" and not bool(task.resolution.strip()):
                    messages.error(request, 'Please provide resolution before closing.')
                    return redirect('task:edittask', task_id=task.pk)
                task.user = request.user
                task.save()
            return redirect('task:task_detail', task_id=task.pk)
    else:
        form = TaskForm(instance=task)
    context = {'form': form, 'task_id': task_id}
    return render(request, 'management/task_edit.html', context)


@login_required(login_url='/login')
def task_detail(request, task_id):
    """this view shows tasks details and all its
        associated comments ordered by created date desc"""
    task = get_object_or_404(Task, pk=task_id)
    comments = Comment.objects.filter(task=task).order_by('-created_date')
    form = CommentForm()
    context = {'form': form, 'comments': comments, 'task': task}
    return render(request, 'management/task_detail.html', context)


@login_required(login_url='/login')
def search(request):
    """ search view """
    search_text = request.GET['srcStr']
    # Ensure search string is submitted and is min 3 char
    if not search_text and len(search_text) < 3:
        messages.error(request, 'Search string should be greater than 2 characters')
    else:
        tasks = TaskTable(Task.objects.filter(
            Q(title__contains=search_text) | Q(description__contains=search_text) | Q(status=search_text)))
        RequestConfig(request, paginate={'per_page': 20}).configure(tasks)
        print(tasks)
        context = {
            'tasks': tasks,
            'search': search_text,
        }
        return render(request, 'management/search_results.html', context)


@login_required(login_url='/login')
def taskactivity(request):
    """ take user to taskactivity.html where we do
        AJAX request to get chartdata JSON """
    return render(request, 'management/taskactivity.html')


@login_required(login_url='/login')
def chartdata(request):
    """ this view is called via XMLHttpRequest from chart.js
        This data is used for creating reports admins get metrics for all tasks """
    username = request.user

    if request.user.is_superuser:
        task_list = Task.objects.all()
    else:
        task_list = Task.objects.filter(user=username)
    # get count for each statuses which is required for chart.js to display reports
    task_count = task_list.count()
    task_to_do = task_list.filter(status='To Do').count()
    task_in_progress = task_list.filter(status='In Progress').count()
    task_blocked = task_list.filter(status='Blocked').count()
    task_done = task_list.filter(status='Done').count()
    task_dismissed = task_list.filter(status='Dismissed').count()
    labels = ["Tasks", "To Do", "In Progress", "Blocked", "Done", "Dismissed"]
    default_items = [task_count, task_to_do, task_in_progress, task_blocked, task_done, task_dismissed]
    data = {
        "labels": labels,
        "default": default_items,
    }
    return JsonResponse(data)
