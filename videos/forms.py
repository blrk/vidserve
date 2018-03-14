from django.contrib.auth.models import User
from .models import Video
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'contatct-form'}))

    class Meta:
        model = User
        fields = ['username','email','password',]

class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password',]

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('video_title', 'file_file',)
