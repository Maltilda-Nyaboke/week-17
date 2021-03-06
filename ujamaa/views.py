from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import *
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .email import send_welcome_email
from .models import *

# Create your views here.

def home(request):
    if request.method == 'POST':
        form = NeighborhoodForm(request.POST, request.FILES)
        if form.is_valid():
            neighborhood = form.save(commit=False)
            neighborhood.admin = request.user
            neighborhood.save()
            return redirect('home')
    else:
        form = NeighborhoodForm()
        neighborhoods = Neighborhood.objects.all()
        neighborhoods = neighborhoods[::-1]        
    return render(request, 'index.html',{'form':form, 'neighborhoods':neighborhoods})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            email = form.cleaned_data['email']

            recipient = NewsLetterRecipients(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:    
        form = RegisterForm()
    return render(request, 'register.html',{'form':form}) 

def login_user(request):
    form = AuthenticationForm()
    context = {'form':form}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            return render(request,'registration/login.html',context)  
    else:
        return render(request, 'registration/login.html',context)  

def logout_user(request):
    logout(request)
    return redirect('login')                

def profile(request):
    user = request.user.pk
    profile = Profile.objects.all()
    profile = Profile.objects.filter(user=request.user.pk)
    context = {'profile': profile}
    return render(request, 'profile.html',context)  

def update_profile(request):
    form = UpdateProfileForm()
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile.profile_photo = form.cleaned_data.get('profile_photo')
            profile.bio = form.cleaned_data.get('bio')
            profile.save()
            return redirect('profile')
        else:
            form = UpdateProfileForm() 
    return render(request, 'update_profile.html',{'form':form}) 

def search(request):
    query = request.GET.get('query')
    if query:
        business = Business.objects.filter(
            Q(name__icontains=query)
        )
        context = {'business': business}
        return render(request, 'search.html',context) 
def neighborhood(request,id):
    neighborhood = Neighborhood.objects.get(id=id)
    current_user = request.user
    business = Business.objects.filter(neighborhood=neighborhood)
    users = Profile.objects.filter(neighborhood=neighborhood)
    posts = Post.objects.filter(neighborhood=neighborhood)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES,prefix="post_form")
        business_form = BusinessForm(request.POST, request.FILES,prefix='business_form')
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.neighborhood = neighborhood
            post.user = request.user
            post.save()
        elif business_form.is_valid():
            business = business_form.save(commit=False)
            business.neighborhood = neighborhood
            business.user = request.user
            business.save()
        else:    
            post_form = PostForm(prefix='post_form')
            business_form = BusinessForm(prefix='business_form')
        return redirect('neighborhood',id)
    else:
        post_form = PostForm(prefix='post_form')
        business_form = BusinessForm(prefix='business_form')
    context ={
                'post_form':post_form,
                'business_form': business_form,
                'current_user':current_user,
                'neighborhood':neighborhood,
                'business':business,
                'users':users,
                'posts':posts
        }
    return render(request, 'neighborhood.html',context)

def join_hood(request,id):
    neighborhood = get_object_or_404(Neighborhood, id=id)
    request.user.profile.neighborhood = neighborhood
    request.user.profile.save()
    return redirect('neighborhood', id = neighborhood.id) 


def leave_hood(request,id):
    neighborhood = get_object_or_404(Neighborhood, id=id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    return redirect('home')
