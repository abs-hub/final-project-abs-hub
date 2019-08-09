from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Task


# standard signup form fields to be shown when user tries to register
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# user login form
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# Task form which has user reference shown as model choice form
class TaskForm(forms.ModelForm):
    deadline = forms.DateField(widget=forms.DateInput(format='%m/%d/%Y', attrs={'placeholder': 'mm/dd/yyyy',
                                                                                'pattern': '\d{1,2}/\d{1,2}/\d{4}'}),
                               input_formats=('%m/%d/%Y',),
                               required=True)

    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  to_field_name='id',
                                  empty_label="Select User")

    class Meta:
        model = Task
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 70}),
            'resolution': forms.Textarea(attrs={'rows': 3, 'cols': 70}),
        }
        fields = ('title', 'user', 'status', 'priority', 'description', 'resolution', 'deadline')


# comment form with comment_description field shown
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_description']
