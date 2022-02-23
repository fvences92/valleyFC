from django.shortcuts import render, redirect
from .models import Player
from django.contrib.auth.forms import UserCreationForm


# environment variables
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'valleyfc'


# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')


# Add new view
def players_index(request):
    
    return render(request, 'players/index.html', { 'Player': Player})
