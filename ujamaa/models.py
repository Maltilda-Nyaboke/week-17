from pydoc import describe
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django import forms


# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=30)
    posted = models.DateTimeField(auto_now_add=True)

    def save_location(self):
        self.save()

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    name = models.CharField(max_length=75)
    image =models.ImageField(upload_to='images')
    description = models.TextField(null=True)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    occupants_count = models.IntegerField(default=0)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


    def create_neigborhood(self):
        self.save()

    @classmethod
    def delete_neighbourhood(cls, id):
        cls.objects.filter(id=id).delete()

    def update_neigborhood(self):
        self.update()        
    def update_occupants(self):
        self.update() 


    @classmethod
    def search_by_name(cls, search_term):
        hood = cls.objects.filter(name__icontains=search_term)
        return hood   

    @classmethod
    def find_neigborhood(cls, id):
        hood = cls.objects.get(id=id)
        return hood     

    def __str__(self):
        return self.name     

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo =models.ImageField(upload_to='images')
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE,null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    joined=models.DateTimeField(auto_now=True)

    def save_profile(self):
        self.save()
    
    def delete_profile(self):
        self.delete()
    
    def update(self):
        self.save()    
   
   
    def __str__(self):
        return self.contact


class Business(models.Model):
    name = models.CharField(max_length=50)
    image =models.ImageField(upload_to='images',null=False)
    email = models.EmailField(max_length=50)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    def update_business(self):
        self.update()   

    def __str__(self):
        return self.name     

class Post(models.Model):
    title = models.CharField(max_length=50)
    image =models.ImageField(upload_to='images')
    content = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, default=1)
    posted = models.DateTimeField(auto_now_add=True)    

    def create_post(self):
        self.save()

    def delete_post(self):
        self.delete()

    def update_post(self):
        self.update()
    
    def __str__(self):
        return self.content

class NewsLetterRecipients(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()   
