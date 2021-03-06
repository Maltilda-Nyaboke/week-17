from dataclasses import field
from pyexpat import model
from django import forms
from django.forms import ModelForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *





class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1', 'password2',]

class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')


class UpdateProfileForm(ModelForm):
    class Meta():
        model = Profile
        exclude = ['user']

class BusinessForm(ModelForm):
    class Meta():
        model = Business
        fields = ('name','image', 'email','description')  

class PostForm(ModelForm):
    class Meta():
        model = Post
        fields = ('title','image','content')   


class NeighborhoodForm(ModelForm):
    class Meta():
        model = Neighborhood 
        exclude = ['admin']                 